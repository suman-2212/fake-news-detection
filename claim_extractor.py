import spacy
import os
from serpapi import GoogleSearch
from urllib.parse import urlparse
from sentence_transformers import SentenceTransformer, util

# Load the English language model
try:
    nlp = spacy.load("en_core_web_sm")
    print("spaCy model loaded successfully.")
except OSError:
    print("Downloading spaCy model. Please wait...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    print("spaCy model downloaded and loaded.")

# Load Sentence Transformer model once
print("\nLoading Sentence Transformer model...")
try:
    model_st = SentenceTransformer('all-MiniLM-L6-v2')
    print("Sentence Transformer model loaded successfully.")
except Exception as e:
    print(f"Error loading Sentence Transformer model: {e}")
    print("Please ensure you have internet access for the first run to download the model.")
    model_st = None

def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        entities[ent.label_].append(ent.text)
    return entities

def extract_claims(text):
    doc = nlp(text)
    claims = []
    for sent in doc.sents:
        subj = ""
        verb = ""
        obj = ""
        
        for token in sent:
            if "subj" in token.dep_:
                subj = token.text
            elif token.pos_ == "VERB":
                verb = token.text
            elif "obj" in token.dep_ or token.dep_ == "attr":
                obj = token.text
        
        if subj and verb:
            claim_text = f"{subj} {verb}"
            if obj:
                claim_text += f" {obj}"
            claims.append(claim_text.strip())
            
        # NEW: Always add the full sentence as a claim if it contains entities
        # This helps capture claims that might not fit strict SVO but are verifiable
        if len(sent.ents) > 0 and sent.text.strip() not in claims:
            claims.append(sent.text.strip())
            
    return list(set(claims))

def search_google(query, api_key, entities=None):
    full_query = query

    if entities:
        relevant_entity = ""
        if "PERSON" in entities and entities["PERSON"]:
            relevant_entity = entities["PERSON"][0]
        elif "ORG" in entities and entities["ORG"]:
            relevant_entity = entities["ORG"][0]
        
        if relevant_entity:
            if "ambani" in relevant_entity.lower() or "reliance" in relevant_entity.lower():
                full_query += " site:relianceindustries.com OR site:timesofindia.indiatimes.com OR site:ndtv.com"
            
    print(f"    Generated Google Search Query: '{full_query}'")

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": full_query,
        "hl": "en",
        "gl": "us"
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        return results
    except Exception as e:
        print(f"Error during Google search: {e}")
        return None

def verify_claim_with_results(claim, search_results, semantic_model=None, similarity_threshold=0.5):
    if semantic_model is None:
        print("    Semantic model not loaded. Skipping semantic verification.")
        return "Fake"

    lower_claim = claim.lower()
    print(f"    Verifying claim: '{claim}' using semantic similarity")

    claim_embedding = semantic_model.encode(claim, convert_to_tensor=True)

    confirming_snippets_count = 0
    contradicting_snippets_count = 0
    
    reliable_domains = [
        "wikipedia.org", ".gov", "pmindia.gov.in", "nytimes.com", "bbc.com", 
        "reuters.com", "cnn.com", "apnews.com", "washingtonpost.com",
        "theguardian.com", "wsj.com", "bloomberg.com", "britannica.com",
        "wildlifesos.org", "nationalgeographic.com", "scientificamerican.com",
        "techcrunch.com", "theverge.com", "ars technica.com", 
        
        # --- NEW: Indian News and Government Domains ---
        "timesofindia.indiatimes.com", "ndtv.com", "zeenews.india.com", 
        "hindustantimes.com", "thehindu.com", "indianexpress.com", 
        "businesstoday.in", "livemint.com", "moneycontrol.com",
        "indiatoday.in", "republicworld.com", "wionews.com",
        "nic.in", "gov.in", # General Indian Government domains
        "pti.in", "ani.in", # Indian news agencies
        # Add more as needed for specific technical/computer domains if relevant for news
        # --- END NEW ---
    ]

    if search_results and 'organic_results' in search_results:
        snippets_to_analyze = []
        for result in search_results['organic_results'][:5]:
            snippet_text = result.get('snippet', '') + " " + result.get('title', '')
            link = result.get('link', '')
            
            if snippet_text.strip():
                snippets_to_analyze.append({'text': snippet_text, 'link': link})

        if not snippets_to_analyze:
            print("      No relevant snippets to analyze for semantic similarity.")
            return "Fake"

        snippet_embeddings = semantic_model.encode([s['text'] for s in snippets_to_analyze], convert_to_tensor=True)

        cosine_scores = util.cos_sim(claim_embedding, snippet_embeddings)[0]

        for i, snippet_info in enumerate(snippets_to_analyze):
            snippet_text = snippet_info['text']
            link = snippet_info['link']
            similarity_score = cosine_scores[i].item()
            
            print(f"        Analyzing search result {i+1} from {link}: Similarity={similarity_score:.4f}")
            print(f"          Snippet: {snippet_text[:150]}...")
            
            parsed_url = urlparse(link)
            domain = parsed_url.netloc
            is_reliable_source = any(rd in domain for rd in reliable_domains)
            print(f"          Extracted domain: {domain}, Is reliable source: {is_reliable_source}")

            # NEW: More nuanced confirmation if a source is generally trustworthy but not in our explicit list
            is_generally_trustworthy = is_reliable_source or ("news" in domain or "report" in domain or "press" in domain)

            if similarity_score >= similarity_threshold and is_generally_trustworthy:
                if any(neg_word in snippet_text.lower() for neg_word in ["not", "false", "incorrect", "no evidence", "denied", "refuted", "rumor", "hoax"]):
                    print(f"          *** POTENTIAL CONTRADICTION within a highly similar, trustworthy snippet. ***")
                    contradicting_snippets_count += 1
                else:
                    print(f"          *** STRONG CONFIRMATION FOUND from trustworthy source! ***")
                    confirming_snippets_count += 1
            elif similarity_score > 0.4 and any(neg_word in snippet_text.lower() for neg_word in ["not", "false", "incorrect", "denied", "refuted", "rumor", "hoax"]) and is_generally_trustworthy:
                print(f"          *** EXPLICIT CONTRADICTION FOUND from a trustworthy source! ***")
                contradicting_snippets_count += 1
            else:
                print(f"          No strong confirmation or contradiction from this snippet (Sim: {similarity_score:.2f}, Reliable: {is_reliable_source}, Trustworthy: {is_generally_trustworthy}).")

    print(f"    Summary: Confirmations: {confirming_snippets_count}, Contradictions: {contradicting_snippets_count}")

    # Final Verdict Logic - Highly tuned for high confidence 'Real' detection
    if confirming_snippets_count > contradicting_snippets_count and confirming_snippets_count > 0:
        # Ensure a strong positive signal
        if confirming_snippets_count >= 2: # At least two strong confirmations
            print("    VERDICT LOGIC: Multiple strong confirmations, minimal contradictions. => Real")
            return "Real"
        elif confirming_snippets_count == 1 and contradicting_snippets_count == 0 and similarity_threshold > 0.6: # Single strong confirmation if similarity is very high
            print("    VERDICT LOGIC: Single very strong confirmation, no contradictions. => Real")
            return "Real"
        else:
            print("    VERDICT LOGIC: Some confirmations, but not strong enough for 'Real'. => Fake (conservative)")
            return "Fake"
    elif contradicting_snippets_count > 0:
        print("    VERDICT LOGIC: Found contradictions. => Fake")
        return "Fake"
    else:
        print("    VERDICT LOGIC: No strong confirmations or clear dominance of either. Defaulting to Fake.")
        return "Fake" # Default to Fake (conservative)

if __name__ == "__main__":
    # Try to get API key from environment variable or prompt user
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    if not SERPAPI_API_KEY:
        print("\n--- SerpApi API Key Required ---")
        print("Please get your API key from https://serpapi.com/ and set it as an environment variable (SERPAPI_API_KEY) or enter it here for this session.")
        SERPAPI_API_KEY = input("Enter your SerpApi API Key: ")
        if not SERPAPI_API_KEY:
            print("API Key not provided. Exiting.")
            exit()

    print("\n--- Testing Claim Extractor ---")
    sample_news_1 = "Indian prime minister is Narendra Modi. He visited France last week."
    sample_news_2 = "The Earth is flat and the moon is made of cheese. Scientists confirm this today."
    sample_news_3 = "India's prime minister is Vijay Prasath."

    print(f"\nAnalyzing: '{sample_news_1}'")
    entities_1 = extract_entities(sample_news_1)
    claims_1 = extract_claims(sample_news_1)
    print(f"  Entities: {entities_1}")
    print(f"  Claims: {claims_1}")

    if claims_1 and model_st:
        print("  Performing web searches for claims...")
        for i, claim in enumerate(claims_1):
            print(f"    Searching for Claim {i+1}: '{claim}'")
            search_results = search_google(claim, SERPAPI_API_KEY, entities_1)
            if search_results and 'organic_results' in search_results:
                print(f"      Top 3 search results for '{claim}':")
                for j, result in enumerate(search_results['organic_results'][:3]):
                    title = result.get('title', 'N/A')
                    snippet = result.get('snippet', 'N/A')
                    link = result.get('link', 'N/A')
                    print(f"        {j+1}. {title} - {snippet[:100]}... ({link})")
                verdict = verify_claim_with_results(claim, search_results, semantic_model=model_st)
                print(f"      Verdict for '{claim}': {verdict}")
            else:
                print(f"      No significant search results found for '{claim}'.")
    else:
        print("  No claims extracted or semantic model not loaded for sample 1.")

    print(f"\nAnalyzing: '{sample_news_2}'")
    entities_2 = extract_entities(sample_news_2)
    claims_2 = extract_claims(sample_news_2)
    print(f"  Entities: {entities_2}")
    print(f"  Claims: {claims_2}")

    if claims_2 and model_st:
        print("  Performing web searches for claims...")
        for i, claim in enumerate(claims_2):
            print(f"    Searching for Claim {i+1}: '{claim}'")
            search_results = search_google(claim, SERPAPI_API_KEY, entities_2)
            if search_results and 'organic_results' in search_results:
                print(f"      Top 3 search results for '{claim}':")
                for j, result in enumerate(search_results['organic_results'][:3]):
                    title = result.get('title', 'N/A')
                    snippet = result.get('snippet', 'N/A')
                    link = result.get('link', 'N/A')
                    print(f"        {j+1}. {title} - {snippet[:100]}... ({link})")
                verdict = verify_claim_with_results(claim, search_results, semantic_model=model_st)
                print(f"      Verdict for '{claim}': {verdict}")
            else:
                print(f"      No significant search results found for '{claim}'.")
    else:
        print("  No claims extracted or semantic model not loaded for sample 2.")

    print(f"\nAnalyzing: '{sample_news_3}'")
    entities_3 = extract_entities(sample_news_3)
    claims_3 = extract_claims(sample_news_3)
    print(f"  Entities: {entities_3}")
    print(f"  Claims: {claims_3}")

    if claims_3 and model_st:
        print("  Performing web searches for claims...")
        for i, claim in enumerate(claims_3):
            print(f"    Searching for Claim {i+1}: '{claim}'")
            search_results = search_google(claim, SERPAPI_API_KEY, entities_3)
            if search_results and 'organic_results' in search_results:
                print(f"      Top 3 search results for '{claim}':")
                for j, result in enumerate(search_results['organic_results'][:3]):
                    title = result.get('title', 'N/A')
                    snippet = result.get('snippet', 'N/A')
                    link = result.get('link', 'N/A')
                    print(f"        {j+1}. {title} - {snippet[:100]}... ({link})")
                verdict = verify_claim_with_results(claim, search_results, semantic_model=model_st)
                print(f"      Verdict for '{claim}': {verdict}")
            else:
                print(f"      No significant search results found for '{claim}'.")
    else:
        print("  No claims extracted or semantic model not loaded for sample 3.")

    print("\n--- Test Claim Extractor with your own text (with Web Search) ---")
    while True:
        user_text = input("Enter a news sentence or phrase (or type 'exit' to quit): ")
        if user_text.lower() == 'exit':
            break
        if user_text:
            entities = extract_entities(user_text)
            claims = extract_claims(user_text)
            print(f"  Entities: {entities}")
            print(f"  Claims: {claims}")

            if claims and model_st:
                print("  Performing web searches for claims...")
                final_news_verdict = "Real" # Default to real, change to fake if any claim is fake
                for i, claim in enumerate(claims):
                    print(f"    Searching for Claim {i+1}: '{claim}'")
                    search_results = search_google(claim, SERPAPI_API_KEY, entities)
                    if search_results and 'organic_results' in search_results:
                        print(f"      Top 3 search results for '{claim}':")
                        for j, result in enumerate(search_results['organic_results'][:3]):
                            title = result.get('title', 'N/A')
                            snippet = result.get('snippet', 'N/A')
                            link = result.get('link', 'N/A')
                            print(f"        {j+1}. {title} - {snippet[:100]}... ({link})")
                        verdict = verify_claim_with_results(claim, search_results, semantic_model=model_st)
                        print(f"      Verdict for '{claim}': {verdict}")
                        if verdict == "Fake":
                            final_news_verdict = "Fake"
                            break # If any claim is fake, the whole news is fake
                    else:
                        print(f"      No significant search results found for '{claim}'.")
                        final_news_verdict = "Fake" # No search results implies unverified/fake
                print(f"\nFINAL NEWS VERDICT: {final_news_verdict}")
            else:
                print("  No claims extracted or semantic model not loaded. Defaulting to Fake.")
                print(f"\nFINAL NEWS VERDICT: Fake")

        else:
            print("Please enter some text.")

    print("Exiting claim extractor.")

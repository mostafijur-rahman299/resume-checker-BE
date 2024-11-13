import spacy
from spacy.matcher import PhraseMatcher


class ResumeParser:
    def __init__(self):
        # Load the language model
        self.nlp = spacy.load("en_core_web_sm")
        # Define a list of skills for rule-based matching
        self.skills = ["Python", "Django", "React", "JavaScript", "SQL"]
        self.matcher = PhraseMatcher(self.nlp.vocab)
        patterns = [self.nlp.make_doc(skill) for skill in self.skills]
        self.matcher.add("SKILLS", patterns)

    def process_text(self, text):
        # Process the resume text with spaCy
        doc = self.nlp(text)
        return doc

    def extract_data(self, doc):
        resume_data = {
            "name": self.extract_name(doc),
            "contact": self.extract_contact_info(doc),
            "experience": self.extract_experience(doc),
            "education": self.extract_education(doc),
            "skills": self.extract_skills(doc)
        }
        return resume_data

    def extract_name(self, doc):
        # Extract name using NER (Person entity)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def extract_contact_info(self, doc):
        contact_info = {
            "email": None,
            "phone": None
        }
        for ent in doc.ents:
            if ent.label_ == "EMAIL":
                contact_info["email"] = ent.text
            elif ent.label_ == "PHONE":
                contact_info["phone"] = ent.text
        return contact_info

    def extract_experience(self, doc):
        experience = []
        # Example: Look for job titles and companies
        for ent in doc.ents:
            if ent.label_ == "ORG":  # Companies
                experience.append({"company": ent.text, "title": "Unknown", "dates": "Unknown"})
        return experience

    def extract_education(self, doc):
        education = []
        for ent in doc.ents:
            if ent.label_ == "ORG":  # Extract University
                education.append({"degree": "Unknown", "institution": ent.text, "year": "Unknown"})
        return education

    def extract_skills(self, doc):
        skills = []
        # Run the phrase matcher to extract skills
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            skills.append(matched_span.text)
        return skills

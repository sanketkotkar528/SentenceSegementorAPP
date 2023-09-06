from langchain.chat_models import AzureChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import json
import unicodedata, re

class Sentence_Segmentor():
    prompt = """
    
        Your job is as smart assistance is to break sentence logically.
        The sentence or para will be given in {para} below.

        Examples of sentence breaking :-

        1) Sentence :- Serum AST and bilirubin ≤ 1.5 times the upper limit of normal.
                
                Segment 1:- Serum AST ≤ 1.5 times the upper limit of normal.
                Segment 2:- Bilirubin ≤ 1.5 times the upper limit of normal.

        2) Sentence :- Complete Blood Count (CBC), Chemistry Panel (CMP) and Coagulation Panel (PT, & INR) no greaternthan 4 weeks prior to registrations.

                Segment 1:- Complete Blood Count (CBC) no greater than 4 weeks prior to registration.
                Segment 2:- Chemistry Panel (CMP) no greater tha 4 weeks prior to registration.
                Segment 3:- Coagulation Panel (PT, & INR) no greater than 4 weeks prior to registration.

        3) Sentence :- Patient age between 30 and 50.

                Segment 1:- Patient age between 30 and 50.

        4) Sentence :- Chronic excessive use of psychopharmaceuticals, alcohol, illicit drugs, or narcotics.

                Segment 1:- Chronic excessive use of psychopharmaceuticals.
                Segment 2:- Chronic excessive use of alcohol.
                Segment 3:- Chronic excessive use of illicit drug, or narcotics.

        While breaking sentences you should break the sentence into smaller sentences but newly formed sentences
        should be logical and meangful. Only rewrite sentence if you break into small parts.
        Newly created sentece should retain original meaning of the input sentence even after breaking.

        To break sentences logically follow below steps:

        Step 1:- Identify if given text has bullet points or it is a complete paragraph or it contains combination of para and bullet points.
        Step 2:- If found bullet points then create individual sentences for each bullet point. If no bullet point found process Step 4 directly.
        Step 3:- This step is only if bullet points are found. In this step you will analyse if sentences identified in Step 2 based on bullet points
                has multiple sentences. If found such situaltion break sentences based on fullstops that terminate sentences. Remove bullet points characters.
        Step 4:- Identify input sentences. Combine output of Step 3 if Step 3 is applied on input.
        Step 5:- Now for each sentence identified in Step 4 sentence logically into parts. Refer examples of sentence breaking for the same.
        Step 6:- Create the short description in 50 words based on what input text is talking about in simple words.
        Step 7:- While creating description add Disclaimer about that you are a bot and some times you might have some bias for creating short descriptions
                based on text.

        Final and only output should be a json object as mentioned below with Bot message as success,
        if any erorrs return empty json object and bot message as error.

                Identified type : Result of Step 1.
                Input Sentences : Result of Step 4.
                Logical broken sentences : Result of Step 5.
                Short Description : Result of Step 6.
                Disclaimer : Disclaimer Generated in Step 7.
                Bot message :

        """


    def __init__(self) -> None:
        self.llm_GPT_3 = AzureChatOpenAI(
            openai_api_type='azure',
            openai_api_key="dfe8fa3f42104388a15a81eefc924c84",
            openai_api_base="https://genaiexamples.openai.azure.com/",
            openai_api_version="2023-05-15",
            deployment_name="chatgpt35",
            temperature=0,
            verbose=True
        )


    def remove_escape_sequences(self, string):
        return string.encode("utf-8").decode("unicode_escape")
    
    def get_responce(self, input_text):

        try:
            prompt_chain = PromptTemplate.from_template(self.prompt)
            llm_chain = LLMChain(llm=self.llm_GPT_3,
                                 prompt=prompt_chain)
            
            processed_text = unicodedata.normalize('NFKD', input_text)
            processed_text = re.sub(r"\n", "", processed_text)
            processed_text = re.sub(r"\t", "", processed_text)
            processed_text = re.sub(r"[ ]{2,}", "", processed_text)
            processed_text = re.sub(r"-", "", processed_text)
        
            responce = llm_chain.run(para=input_text)
            print("Responce:", responce)
            return json.load(responce)
        
        except Exception as e:
            print(e)
            return False

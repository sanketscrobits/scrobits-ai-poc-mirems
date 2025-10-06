from vector_store.vector_index_strategies.base import VectorIndexStrategy
from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain.text_splitter import CharacterTextSplitter
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from src.config.settings import ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT, ASTRA_DB_COLLECTION_NAME, GEMINI_API_KEY, ASTRA_DB_ID
# from llama_index.core import StorageContext, VectorStoreIndex

from dotenv import load_dotenv
from os import getenv
from pathlib import Path

load_dotenv(".env")

BASE_DIR = Path(__file__).resolve().parent.parent

ASTRA_DB_APPLICATION_TOKEN=getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT=getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_COLLECTION_NAME=getenv("ASTRA_DB_COLLECTION_NAME")
EMBEDDING_DIMENSION=getenv("EMBEDDING_DIMENSION", '768')
ASTRA_DB_ID=getenv("ASTRA_DB_ID")
GEMINI_API_KEY=getenv("GEMINI_API_KEY")

from typing import List
import os

import cassio



class AstraDBVectorIndex(VectorIndexStrategy):
    def __init__(self, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT,ASTRA_DB_COLLECTION_NAME,ASTRA_DB_ID, GEMINI_API_KEY):
        self._vector_index=None
        self._llm=None
        self._llm = ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY, model="gemini-1.5-flash")
        embedding = GoogleGenerativeAIEmbeddings(google_api_key=GEMINI_API_KEY, model="models/embedding-001")
        cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)
        raw_text="'GOVERNMENT OF INDIA\nBUDGET 2025-2026\nSPEECH\nOF\nNIRMALA SITHARAMAN\nMINISTER OF FINANCE\nFebruary 1,  2025 \nCONTENTS  \n \nPART – A \n Page No.  \nIntroduction  1 \nBudget Theme  1 \nAgriculture as the 1st engine  3 \nMSMEs as the 2nd engine  6 \nInvestment as the 3rd engine  8 \nA. Investing in People  8 \nB. Investing in  the Economy  10 \nC. Investing in Innovation  14 \nExports as the 4th engine  15 \nReforms as the Fuel  16 \nFiscal Policy  18 \n \n \nPART – B \nIndirect taxes  20 \nDirect Taxes   23 \n \nAnnexure to Part -A 29 \nAnnexure to Part -B 31 \n \n   \n \nBudget 202 5-2026 \n \nSpeech of  \nNirmala Sitharaman  \nMinister of Finance  \nFebruary 1 , 202 5 \nHon’ble Speaker,  \n I present the Budget for 2025 -26. \nIntroduction  \n1. This Budget continues our Government ’s efforts to:  \na) accelerate growth,  \nb) secure inclusive development,  \nc) invigorate private sector investments,  \nd) uplift household sentiments, and \ne) enhance spending power of India’s rising middle class.  \n2. Together, we embark on a journey to unlock our nation’s tremendous \npotential for greater prosperity and global positioning under the leadership of \nHon’ble Prime Minister Shri Narendra Modi.  \n3. As we complete the first quarter of the 21st century, continuing \ngeopolitical headwinds suggest lower  global economic growth over the \nmedium term. However, our aspiration for a Viksit Bharat inspires us, and the \ntransformative work we have done during our Government ’s first two terms \nguides us, to march forward resolutely.  \nBudget Theme  \n4. Our economy is the fastest -growing among all major global economies. \nOur development track record of the past 10 years and structural reforms have \ndrawn global attention. Confidence in India’s capability and potential has only  2  \n \ngrown in this period. We see the next five years as a unique opportunity to \nrealize ‘Sabka Vikas’, stimulating balanced growth of all regions.  \n5. The great Telugu poet and playwright Gurajada Appa Rao had said, \n‘Desamante Matti Kaadoi, Desamante Manushuloi ’; meaning, ‘A country is not \njust its soil, a country is its people.’ In line with this, for us, Viksit Bharat, \nencompasses:  \na) zero -poverty;  \nb) hundred per cent good quality school education;   \nc) access to high -quality, affordable, and comprehensive healthcare;  \nd) hundred per cent skilled labour with meaningful employment;  \ne) seventy per cent women in economic activities; and  \nf) farmers making our country the ‘food basket of the world’.  \n6. In this Budget, the proposed development measures span ten broad \nareas focusing on Garib, Youth, Annadata and Nari.  \n1) Spurring Agricultural Growth and Productivity;  \n2) Building Rural Prosperity and Resilience;  \n3) Taking Everyone Together on an Inclusive Growth path;  \n4) Boosting Manufacturing and Furthering Make in India;  \n5) Supporting MSMEs;  \n6) Enabling Employment -led Development;  \n7) Investing in people, economy and innovation;  \n8) Securing Energy Supplies;  \n9) Promoting Exports; and  \n10) Nurturing Innovation . \n7. For this journey of development,  \na) Our four powerful engines are: Agriculture, MSME, Investment, and \nExports  \nb) The fuel: our Reforms  \nc) Our guiding spirit: Inclusivity  \nd) And the destination: Viksit Bharat   3  \n \n8. This Budget aims to initiate transformative reforms across six domains. \nDuring the next five years, these will augment our growth potential and global \ncompetitiveness. The domains are:  \n1) Taxation;  \n2) Power Sector;  \n3) Urban Development;  \n4) Mining;  \n5) Financial Sector; and  \n6) Regulatory Reforms.  \nAgriculture as the 1st Engine  \n9. Now I move to specific proposals, beginning with ‘Agriculture as the 1st \nEngine’.  \nPrime Minister Dhan -Dhaanya Krishi Yojana - Developing Agri Districts \nProgramme  \n10. Motivated by the success of the Aspirational Districts Programme, our \nGovernment  will undertake a ‘Prime Minister Dhan -Dhaanya Krishi Yojana ’ in \npartnership with states. Through the convergence of existing schemes and \nspecialized measures, the programme will cover 100 districts with low \nproductivity, moderate crop intensity and below -average credit parameters. It \naims to (1) enhance agricultural  productivity, (2) adopt crop diversification and \nsustainable agriculture practices, (3) augment post -harvest stor age at the \npanchayat and block level, (4) improve irrigation facilities, and (5) facilitate \navailability of long -term and short -term credit. This programme is likely to help \n1.7 crore farmers.  \nBuilding Rural Prosperity and Resilience  \n11. A comprehensive multi -sectoral ‘Rural Prosperity and Resilience’ \nprogramme will be launched in partnership with states. This will address under -\nemployment in agriculture through skilling, investment, technology, and \ninvigorating the rural economy. The goal  is to generate ample opportunities in \nrural areas so that migration is an option, but not a necessity.  \n12. The programme will focus on rural women, young farmers, rural youth, \nmarginal and small farmers, and landless families. Details are in Annexure A.   4  \n \n13. Global and domestic best practices will be incorporated and \nappropriate technical and financial assistance will be sought from multilateral \ndevelopment banks. In Phase -1, 100 developing agri -districts will be covered.   \nAatmanirbharta in Pulses    \n14. Our Government  is implementing the National Mission for Edible \nOilseed for achieving atmanirbhrata in edible oils. Our farmers have the \ncapability to grow enough for our needs and more.  \n15. Ten years ago, we made concerted efforts and succeeded in achieving \nnear self -sufficiency in pulses. Farmers responded to the need by increasing the \ncultivated area by 50 per cent and Government  arranged for procurement and \nremunerative prices. Since then, with rising incomes and better affordability, \nour consumption of pulses has increased significantly.  \n16. Our Government  will now launch a 6 -year “Mission for Aatmanirbharta \nin Pulses” with a special focus on Tur, Urad and Masoor.  Details are in \nAnnexure B. Central agencies (NAFED and NCCF) will be ready to procure these \n3 pulses, as much as offered during the next 4 years  from farmers who register \nwith these agencies and enter into agreements.   \nComprehensive Programme for Vegetables & Fruits  \n17. It is encouraging that our people are increasingly becoming aware of \ntheir nutritional needs. It is a sign of a society becoming healthier. With rising \nincome levels, the consumption of vegetables, fruits and shree -anna is \nincreasing significantly. A compr ehensive programme to promote production, \nefficient supplies, processing, and remunerative prices for farmers will be \nlaunched in partnership with states. Appropriate institutional mechanisms for \nimplementation and participation of farmer producer organiza tions and \ncooperatives will be set up.   \nMakhana Board in Bihar  \n18. For this, there is a special opportunity for the people of Bihar. A \nMakhana Board will be established in the state to improve production, \nprocessing, value addition, and marketing of makhana. The people engaged in \nthese activities will be organized into FP Os. The Board will provide handholding \nand training support to makhana farmers and will also work to ensure they \nreceive the benefits of all relevant Government  schemes.     5  \n \nNational Mission on High Yielding Seeds  \n19. A National Mission on High Yielding Seeds will be launched, aimed at (1) \nstrengthening the research ecosystem, (2) targeted development and \npropagation of seeds with high yield, pest resistance and climate resilience, and \n(3) commercial availability of mor e than 100 seed varieties released since July \n2024.  \nFisheries  \n20. India ranks second -largest globally in fish production and aquaculture. \nSeafood exports are valued at ` 60 thousand crore. To unlock the untapped \npotential of the marine sector, our Government  will bring in an enabling \nframework for sustainable harnessing of fisheries from Indian Exclusive \nEconomic Zone and High Seas, with a special focus on the Andaman & Nicobar \nand Lakshadweep Islands.  \nMission for Cotton Productivity  \n21. For the benefit of lakhs of cotton growing farmers, I am pleased to \nannounce a ‘Mission for Cotton Productivity’. This 5 -year mission will facilitate \nsignificant improvements in productivity and sustainability of cotton farming, \nand promote extra -long stap le cotton varieties. The best of science & \ntechnology support will be provided to farmers. Aligned with our integrated 5F \nvision for the textile sector, this will help in increasing incomes of the farmers, \nand ensure a steady supply of quality cotton for r ejuvenating India’s traditional \ntextile sector."
        astra_vector_store = Cassandra(
            embedding=embedding,
            table_name="qa_mini_demo",
            session=None,
            keyspace=None,
        )
        text_splitter = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 80,
            chunk_overlap  = 20,
            length_function = len,
        )
        texts = text_splitter.split_text(raw_text)
        astra_vector_store.add_texts(texts[:50])
        print("Inserted %i headlines." % len(texts[:50]))
        self._vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

        # self.embeddings = embeddings
        # self._collection = AstraDBVectorStore(
        #     token=ASTRA_DB_APPLICATION_TOKEN,
        #     api_endpoint=ASTRA_DB_API_ENDPOINT,
        #     collection_name=ASTRA_DB_COLLECTION_NAME,
        #     embedding=self.embeddings,
        # )
        
    def create_or_load_vectorstore(self, documents=None):
        self.vector_store.add_documents(documents)
        
    def query(self, text: List[float], top_k: int) -> List[str]:

        answer = self._vector_index.query(text, llm=self._llm).strip()
        return answer

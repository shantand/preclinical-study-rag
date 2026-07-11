# Preclinical Study RAG

An end-to-end Retrieval-Augmented Generation (RAG) application that answers questions over **preclinical toxicology studies** and **regulatory guidelines** using semantic search.

The project demonstrates the core building blocks of a RAG system:

- PDF ingestion
- Text chunking
- Embedding generation
- Vector database (ChromaDB)
- Semantic retrieval
- LLM-powered answer generation
---

## Motivation

Researchers frequently need to answer questions such as:

- How are 28-day oral toxicity studies typically designed?
- Which animal models are commonly used?
- What endpoints are measured across different studies?
- How do published studies compare with OECD/FDA guidance?

Instead of manually reading multiple papers, this application retrieves the most relevant document chunks and uses an LLM to generate an evidence-based answer.

---

## Architecture

```
                PDFs
                  │
                  ▼
          ingest.py
                  │
                  ▼
          chunks.json
                  │
                  ▼
        vectorise.py
                  │
                  ▼
        Chroma Vector DB
                  │
                  ▼
            chat.py
                  │
                  ▼
      Semantic Retrieval
                  │
                  ▼
             OpenAI LLM
                  │
                  ▼
            Grounded Answer
```

---

## Tech Stack

| Component |   Technology |
|----------|------------|
| Language | Python 3.12 |
| PDF Parsing | PyMuPDF |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Database | ChromaDB |
| LLM | OpenAI |
| Retrieval | Cosine Similarity Search |

---

## Project Structure

```
preclinical-study-rag/

├── data/
├── output/
├── chroma_db/
│
├── ingest.py
├── vectorise.py
├── chat.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

Create a virtual environment.

```bash
python3.12 -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Prepare Dataset

Place all PDFs inside the `data/` directory. For running this experiment we have got the data from the https://pmc.ncbi.nlm.nih.gov/?utm_source=chatgpt.com which have open access pdfs.

Example:

```
data/

OECD407.pdf
ICH_M3.pdf
study1.pdf
study2.pdf
...
```

The repository intentionally does **not** include PDFs because many scientific papers are copyrighted.

---

## Step 1 — Extract and Chunk PDFs

```bash
python ingest.py
```

This generates:

```
output/chunks.json
```

Each chunk contains:

- document name
- chunk id
- character offsets
- chunk text

---

## Step 2 — Create Vector Database

```bash
python vectorise.py
```

This:

- generates embeddings
- stores them in ChromaDB
- creates the local vector database

---

## Step 3 — Ask Questions

```bash
python chat.py
```

Example:

```
Ask a question:

What biomarkers are commonly measured in repeated-dose toxicity studies?
```

The application first displays the retrieved chunks before generating the final answer.

---

## Example Questions

- Compare study designs across the retrieved studies.

- What biomarkers are commonly measured?

- Which animal species are most frequently used?

- Which organs are evaluated during repeated-dose toxicity studies?

- Summarize the OECD recommendations for 28-day oral toxicity studies.

- Compare the dose ranges used across different studies.

- Which studies reported liver toxicity?

- What endpoints are consistently measured?

---

Ask a question (or 'exit'): What routes of administration are most frequently used?

========== Retrieved Chunks ==========

1. 9789264070684-en.pdf
Distance : 1.6317
 and at least once a week
thereafter, detailed clinical observations should be made in all animals.  These observations should be
made outside the home cage in a standard arena and preferably at the same time of day on each occasion.
They should be carefully recorded, preferably using scoring system
------------------------------------------------------------
2. 9789264070707-en.pdf
Distance : 1.6413
es on each occasion. They should be carefully
recorded, preferably using scoring systems explicitly defined by the testing laboratory.
Effort should be made to ensure that variations in the observation conditions are
minimal. Signs noted should include, but not be limited to, changes in skin, fur, e
------------------------------------------------------------
3. 47459972dft-Generally Accepted Scientific Knowledge in Applications for Drugs Biological Products-Nonclinical.pdf
Distance : 1.6425
............................................................................................................. 1
II.
BACKGROUND ............................................................................................................... 2
A.
Nonclinical Studies and Their Role in Drug Development .
------------------------------------------------------------
4. M3_R2__Guideline.pdf
Distance : 1.6591
ting Authorization for Pharmaceuticals
9
products. It is recommended that these alternative approaches be discussed and agreed
upon with the appropriate regulatory authority.  The use of any of these approaches can
reduce overall animal use in drug development.
Recommended starting doses and maximal
------------------------------------------------------------
5. 47459972dft-Generally Accepted Scientific Knowledge in Applications for Drugs Biological Products-Nonclinical.pdf
Distance : 1.6628
refer to both drugs
under the Federal Food, Drug, and Cosmetic Act and biological products under the Public Health Service Act; and
the term approval is intended to refer to approval and licensure of drug and biological product applications under the
respective authorities.
3 This guidance does not
------------------------------------------------------------
6. 9789264070707-en.pdf
Distance : 1.6767
et
or dissolved in drinking water. The method of oral administration is dependent on the
purpose of the study and the physical/chemical properties of the test material.
15.
Where necessary, the test chemical is dissolved or suspended in a suitable
vehicle. It is recommended that, wherever possible,
------------------------------------------------------------
7. 9789264070707-en.pdf
Distance : 1.6957
e based on the results
of repeated dose or range finding studies and should take into account any existing
toxicological and toxicokinetic data available for the test compound or related materials.
Unless limited by the physical-chemical nature or biological effects of the test chemical,
the highest
------------------------------------------------------------
8. M3_R2__Guideline.pdf
Distance : 1.6970
inical studies or marketing unless there is
significant toxicological concern (e.g., similar target organ toxicity).  This concern would
be modified depending on the margins of safety and the ability to monitor the adverse
effects in humans. If a study is being conducted to address a cause for signi
------------------------------------------------------------
9. M3_R2__Guideline.pdf
Distance : 1.6994
ill
have
product
information
recommendations for co-use with a specific drug, even if not in a fixed combination, and
for which there is minimal clinical information regarding the combination.
Combinations covered might involve: (1) two or more late stage entities (defined as
compounds with signific
------------------------------------------------------------
10. 47459972dft-Generally Accepted Scientific Knowledge in Applications for Drugs Biological Products-Nonclinical.pdf
Distance : 1.7029
 drug's particular mode of administration or
conditions of use.”)
10 See, for example, § 314.50(d)(2).  See also the BLA regulations at 21 CFR part 601, which are silent with respect
to the source of nonclinical data.
Contains Nonbinding Recommendations
Draft — Not for Implementation
3
• Identify sp
------------------------------------------------------------
11. 9789264070707-en.pdf
Distance : 1.7039
observations should be kept for an appropriate period without treatment to detect
persistence of, or recovery from toxic effects.
24.
General clinical observations should be made at least once a day, preferably
at the same time(s) each day, taking into consideration the peak period of anticipated
ef
------------------------------------------------------------
12. main (1).pdf
Distance : 1.7104
y, availability, and safety [1–3]. Often
plants and plants derived products have been a therapeutic tool for
treating disease and health hazards [4]. Nowadays the number of people
affected with complex chronic diseases is increasing and drugs derived
from medicinal plants are being proved to be an e
------------------------------------------------------------

Generating Answer...

========== Answer ==========

Oral administration—typically by gavage, mixed in the diet, or dissolved in drinking water.



## What I Learned

Trade offs that need to be aware of
1. Your use case requires the retrieval of information or search. If not you will be unnecessarily fittting RAG solution to a problem that doesnt demand it.
2. Quality of data is very important. Because if LLM is prevented for hallusinating and asked to used your provided context. Then this boils down to how much quality data you have.
3. During this excercise found out that simply by increasing value of K we were able to provide good context to LLM however in production systems as the value of K increase the token usage will start increasing as well. Thats why rerankers are useful.
4. Data cleaning and transformation could help improve data quality drastically. Like in the above excercise I did not removed the redundant sections like references or introduction from research papers, so, the chunks were carrying garbage information.
5. Search algorithms and distance metrics are main driving factors in any vector search. Algorithm is chosen based on the dataset size and distance metrics are chose based on use case for example - chat based cases requires text handling, and the cosine similarity works best in that case. while if use case demands image retrieval them maybe euclidian distance is more appropriate.
6. Production systems are messier cause it will involve changing data changing business requirement changing infrastructure resources. And hence monitoring would be very crucial.
---



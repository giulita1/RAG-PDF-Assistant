import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class RAGEvaluator:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def similarity(self, text1, text2):

        emb = self.model.encode([text1, text2])

        score = cosine_similarity([emb[0]], [emb[1]])[0][0]

        return score

    def hallucination_score(self, answer, context):

        score = self.similarity(answer, context)

        return score

    def evaluate_record(self, record):

        question = record["question"]
        context = record["context"]
        answer = record["answer"]

        score = self.hallucination_score(answer, context)

        result = {
            "question": question,
            "similarity_score": float(score),
            "possible_hallucination": score < 0.5
        }

        return result


def evaluate_logs(file_path="rag_logs.json"):

    evaluator = RAGEvaluator()

    results = []

    with open(file_path,"r") as f:
        for line in f:

            record = json.loads(line)

            result = evaluator.evaluate_record(record)

            results.append(result)

    return results


def print_summary(results):

    total = len(results)

    hallucinations = sum(1 for r in results if r["possible_hallucination"])

    avg_score = sum(r["similarity_score"] for r in results) / total

    print("Total questions:", total)
    print("Possible hallucinations:", hallucinations)
    print("Hallucination rate:", hallucinations / total)
    print("Average similarity:", avg_score)


if __name__ == "__main__":

    results = evaluate_logs()

    print_summary(results)
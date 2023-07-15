import os
from neo4j_driver import Neo4jConnection, Node
from answer_search import AnswerSearcher
from question_parser import QuestionPaser
from question_classifier import QuestionClassifier
import time
import zhipuai


class Runner:
    def __init__(self):
        self.history = ""
        self.counter = 0
        self.g = Neo4jConnection('neo4j://localhost:7687/', 'neo4j', 'Lorne@2022')
        return
    
    def print_string_with_delay(self, string):
        new_string = string.replace("GLM-130B", "GLM-6B")
        new_string = new_string.replace("GLM模型", "GLM-6B模型")
        for char in new_string:
            print(char, end='')
            time.sleep(0.02)
    
    def llm_request(self, question):
        zhipuai.api_key = "-"
        response = zhipuai.model_api.invoke(
            model="chatglm_std",
            prompt=[
                {"role": "user", "content": question}
            ],
            temperature=0.97
        )
        # print(response)
        if response['code'] == 200:
            return response['data']['choices'][0]['content']
        else: 
            return "超时"

    def ask(self, question):
        classifier = QuestionClassifier()
        parser = QuestionPaser()
        searcher = AnswerSearcher(self.g)
        res_classify = classifier.classify(question)
        if 'args' in res_classify.keys():
            res_cypher = parser.parser_main(res_classify)
            final_answers = searcher.search_main(res_cypher)
            llm_answer = self.llm_request("完善一下这个表述,随机替换一些同义词，不要改变内容的长度:" + final_answers[0])
            self.print_string_with_delay(llm_answer)
            return llm_answer
        else:
            llm_answer = self.llm_request(question)
            self.print_string_with_delay(llm_answer)
            return llm_answer
        
    def ask_must(self, question):
        classifier = QuestionClassifier()
        parser = QuestionPaser()
        searcher = AnswerSearcher(self.g)
        res_classify = classifier.classify(question)
        if 'args' in res_classify.keys():
            res_cypher = parser.parser_main(res_classify)
            final_answers = searcher.search_main(res_cypher)
            self.print_string_with_delay(final_answers[0])
            return final_answers[0]
        else:
            llm_answer = self.llm_request(question)
            self.print_string_with_delay(llm_answer)
            return llm_answer
        
    def ask_no_print(self, question):
        classifier = QuestionClassifier()
        parser = QuestionPaser()
        searcher = AnswerSearcher(self.g)
        res_classify = classifier.classify(question)
        if 'args' in res_classify.keys():
            res_cypher = parser.parser_main(res_classify)
            final_answers = searcher.search_main(res_cypher)
            return final_answers[0]
        else:
            return "找不到"
    
    def clear(self):
        self.history = ""
        self.counter = 0

    def get_question_with_his(self, question):
        return "请根据以下对话历史：\n\n" + self.history + "\n\n回答这个问题：\n" + question
    
    def mem(self, question, ans):
        self.history = self.history + "\n" + question + "\n" + ans
        self.counter = self.counter + 1

    def ask_pro(self, question):
        if self.counter >= 3:
            self.clear()
 
        if self.counter > 0:
            ans = self.ask_no_print(question)
            if ans != "找不到":
                self.mem(question, ans)
                self.print_string_with_delay(ans)
                return
            else:
                new_question = self.get_question_with_his(question)
                ans = self.llm_request(new_question)
                self.mem(question, ans)
                self.print_string_with_delay(ans)
        else:
            ans = self.ask_must(question)
            if not ans == "超时":
                self.mem(question, ans)

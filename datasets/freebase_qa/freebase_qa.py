# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""FreebaseQA: A Trivia-type QA Data Set over the Freebase Knowledge Graph"""


import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{jiang2019freebaseqa,
  title={FreebaseQA: A New Factoid QA Dataset Matching Trivia-Style Question-Answer Pairs with Freebase},
  author={Jiang, Kelvin and Wu, Dekun and Jiang, Hui},
  journal={north american chapter of the association for computational linguistics},
  year={2019}
}
"""

_DESCRIPTION = """\
FreebaseQA is for open-domain factoid question answering (QA) tasks over structured knowledge bases, like Freebase The data set is generated by matching trivia-type question-answer pairs with subject-predicateobject triples in Freebase.
"""

_HOMEPAGE = "https://github.com/kelvin-jiang/FreebaseQA"

_LICENSE = ""


_REPO = "https://raw.githubusercontent.com/kelvin-jiang/FreebaseQA/master/"

_URLs = {
    "train": _REPO + "FreebaseQA-train.json",
    "eval": _REPO + "FreebaseQA-dev.json",
    "test": _REPO + "FreebaseQA-eval.json",
}


class FreebaseQA(datasets.GeneratorBasedBuilder):
    """FreebaseQA: A Trivia-type QA Data Set over the Freebase Knowledge Graph"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "Question-ID": datasets.Value("string"),
                "RawQuestion": datasets.Value("string"),
                "ProcessedQuestion": datasets.Value("string"),
                "Parses": datasets.Sequence({
                    "Parse-Id": datasets.Value("string"),
                    "PotentialTopicEntityMention": datasets.Value("string"),
                    "TopicEntityName": datasets.Value("string"),
                    "TopicEntityMid": datasets.Value("string"),
                    "InferentialChain": datasets.Value("string"),
                    "Answers": datasets.Sequence({
                        "AnswersMid": datasets.Value("string"),
                        "AnswersName": datasets.Sequence([datasets.Value("string")]),
                    }),
                }),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_dir["test"],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["eval"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with open(filepath, encoding="utf-8") as f:
            dataset = json.load(f)

            for data in dataset["Questions"]:
                id_ = data["Question-ID"]
                parses = []
                for item in data["Parses"]:
                    answers = [answer for answer in item["Answers"]]

                    parses.append(
                        {
                            "Parse-Id": item["Parse-Id"],
                            "PotentialTopicEntityMention": item["PotentialTopicEntityMention"],
                            "TopicEntityName": item["TopicEntityName"],
                            "TopicEntityMid": item["TopicEntityMid"],
                            "InferentialChain": item["InferentialChain"],
                            "Answers": answers
                        }
                    )

                yield id_, {
                    "Question-ID": data["Question-ID"],
                    "RawQuestion": data["RawQuestion"],
                    "ProcessedQuestion": data["ProcessedQuestion"],
                    "Parses": parses
                }

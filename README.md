# Search_Engine
To run the the progrem you just need to call main from main.py.

## Configuration info:

```python
-for stemming just call main(stemming=True) the default is stemming=False
-main(orpus_path=corpus_path) with the corpus path on your PC
-main(output_path=output_path) so set the output path on your PC
-adjust the max size of the all buckets before fluse just change MAX_SIZE in posting_handler.py
-adjust the threshold  of the buckets who will flush just change THRESHOLD in posting_handler.py
-adjust the weight of each ranking measure of Glove just change GLOVE_WEIGHT in ranker.py
-adjust the weight of each ranking measure of BM25 just change BM25_WEIGHT in ranker.py
-adjust the weight of each ranking measure of referral-rank just change REFERRAL_WEIGHT in ranker.py
-adjust the weight of each ranking measure of time-rank just change RELEVANCE_WEIGHT in ranker.py
-ConfigClass(corpus_path, number_of_term_buckets=term_buckets, number_of_entities_buckets=entities_buckets) will set the number of number of term and entities buckets
```

## Important info:
```python
-run_engine method we initialize ConfigClass we to have 26 terms buckets and 2 entities buclers
```

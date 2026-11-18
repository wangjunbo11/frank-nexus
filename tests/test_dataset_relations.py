import json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class DatasetRelationsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.records=json.loads((ROOT/'dist/catalog.json').read_text());cls.by_id={x['id']:x for x in cls.records}
 def test_every_dataset_has_a_classification(self):
  for x in self.records:
   if '数据资源' in x['categories']:self.assertIn(x.get('datasetType'),['公开数据集','论文数据集'])
 def test_paper_datasets_have_reciprocal_paper_links(self):
  for x in self.records:
   if x.get('datasetType')=='论文数据集':
    self.assertTrue(x.get('relatedLiteratureIds'))
    for paper_id in x['relatedLiteratureIds']:
     paper=self.by_id[paper_id];self.assertIn(x['id'],paper.get('relatedDataIds',[]))
 def test_requested_paper_has_close_reading_and_reproduction_limits(self):
  paper=next(x for x in self.records if x['url'].endswith('s41560-026-02163-x'))
  self.assertIn('前沿文献',paper['categories']);self.assertGreaterEqual(len(paper.get('reading',[])),8)
  dataset=self.by_id[paper['relatedDataIds'][0]]
  self.assertEqual(dataset['datasetType'],'论文数据集');self.assertIn('商业',json.dumps(dataset,ensure_ascii=False))
if __name__=='__main__':unittest.main()

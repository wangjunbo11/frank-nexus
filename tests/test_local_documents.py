import importlib.util,pathlib,tempfile,unittest,zipfile
import xml.etree.ElementTree as E
path=pathlib.Path(__file__).resolve().parents[1]/'scripts/sync_local_documents.py'
spec=importlib.util.spec_from_file_location('sync',path);sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
W=sync.W
class ReviewImportTests(unittest.TestCase):
 def parse(self,paragraphs):
  root=E.Element(W+'document');body=E.SubElement(root,W+'body')
  for text,level in paragraphs:
   p=E.SubElement(body,W+'p')
   if level is not None:
    pr=E.SubElement(p,W+'pPr');E.SubElement(pr,W+'pStyle',{W+'val':'aa'});n=E.SubElement(pr,W+'numPr');E.SubElement(n,W+'ilvl',{W+'val':str(level)})
   r=E.SubElement(p,W+'r');E.SubElement(r,W+'t').text=text
  with tempfile.TemporaryDirectory() as tmp:
   path=pathlib.Path(tmp)/'review.docx'
   with zipfile.ZipFile(path,'w') as z:z.writestr('word/document.xml',E.tostring(root))
   return sync.import_review(path)
 def source(self,text,refs,heading=False):
  return [('Part I Theory',None),('Chapter',0),('Section',1),(text,None)]+([('参考文献',None)] if heading else [])+[(r,None) for r in refs]
 def refs(self):return ['Li, H. (2026). Groundwater. https://doi.org/10.1/li','Lin, X. (2026). Water. https://doi.org/10.1/lin','Jones, A. (2003). Crops. https://doi.org/10.1/jones']
 def test_untitled_bibliography_is_not_last_section(self):
  parts,refs,audit=self.parse(self.source('Lin等（2026）研究用水。',self.refs()))
  section=parts[0]['chapters'][0]['sections'][0]
  self.assertEqual(len(section['blocks']),1);self.assertEqual(len(refs),3)
  self.assertEqual([r['author'] for r in refs if r['usedIn']],['Lin'])
 def test_heading_and_merged_references(self):
  a,b,c=self.parse(self.source('Li等（2026）研究。',[self.refs()[0]+self.refs()[1],self.refs()[2]],True))
  self.assertEqual(len(b),3);self.assertEqual(c['ambiguous'],[])
 def test_unknown_citation_does_not_get_guessed(self):
  a,b,c=self.parse(self.source('Unknown等（2020）研究。',self.refs()))
  self.assertEqual(c['linkedReferences'],0);self.assertEqual(len(c['unmatched']),1)
 def test_ambiguous_author_year_does_not_get_forced(self):
  refs=['Wang, X. (2026). Irtysh basin. https://doi.org/10.1/a','Wang, H. (2026). Temperature optima. https://doi.org/10.1/b',self.refs()[2]]
  a,b,c=self.parse(self.source('Wang等（2026）研究资源。',refs))
  self.assertEqual(c['linkedReferences'],0);self.assertEqual(len(c['ambiguous']),1)
 def test_fao_alias_maps_to_corporate_author(self):
  refs=['Food and Agriculture Organization of the United Nations. (2021). Water. https://doi.org/10.1/fao',*self.refs()]
  a,b,c=self.parse(self.source('FAO（2021）提出节水建议。',refs))
  self.assertEqual(c['linkedReferences'],1)
if __name__=='__main__':unittest.main()

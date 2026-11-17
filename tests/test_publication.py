import importlib.util,pathlib,unittest
path=pathlib.Path(__file__).resolve().parents[1]/'scripts/check_publication.py';spec=importlib.util.spec_from_file_location('publication',path);publication=importlib.util.module_from_spec(spec);spec.loader.exec_module(publication)
class PublicationGuardTests(unittest.TestCase):
 def test_private_artifacts_are_blocked(self):
  for name in ['dist/notes.json','source-state.json','.local/citation-audit.json']:
   self.assertIn('private artifact',publication.problems(name,b'{}'))
 def test_github_credentials_are_blocked(self):
  self.assertIn('GitHub credential',publication.problems('dist/test.js',('ghp_'+'A'*30).encode()))
 def test_private_keys_are_blocked(self):
  self.assertIn('private key',publication.problems('dist/test.txt',('-----BEGIN '+'PRIVATE KEY-----').encode()))
 def test_local_paths_are_blocked(self):
  self.assertIn('absolute local user path',publication.problems('dist/test.txt',('/'+'Users'+'/researcher/project').encode()))
 def test_normal_public_content_is_allowed(self):
  self.assertEqual(publication.problems('dist/catalog.json',b'{"title":"Nexus","url":"https://doi.org/10.1/example"}'),[])
if __name__=='__main__':unittest.main()

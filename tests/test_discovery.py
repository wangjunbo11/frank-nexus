import datetime,importlib.util,pathlib,unittest
path=pathlib.Path(__file__).resolve().parents[1]/'scripts/discover.py';spec=importlib.util.spec_from_file_location('discovery',path);d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
class DiscoveryTests(unittest.TestCase):
 def test_future_metadata_is_detectable(self):self.assertGreater(d.publication_date({'published':{'date-parts':[[2116,1,1]]}}),datetime.date(2026,11,18))
 def test_online_date_precedes_future_print_issue(self):self.assertEqual(d.publication_date({'published-online':{'date-parts':[[2026,11,10]]},'published-print':{'date-parts':[[2027,1]]}}),datetime.date(2026,11,10))
 def test_ambiguous_nexus_keyword_is_not_enough(self):self.assertFalse(d.relevant_title('The nexus of leadership and learning'))
 def test_resource_nexus_is_relevant(self):self.assertTrue(d.relevant_title('The dual impact of trade on the water-energy-food nexus globally'))
 def test_malformed_dates_are_not_guessed(self):self.assertIsNone(d.publication_date({'published':{'date-parts':[[2026,18,50]]}}))
if __name__=='__main__':unittest.main()

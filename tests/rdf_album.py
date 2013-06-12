# -*- coding: UTF-8 -*-
import os
import datetime
import unittest

from ._rdf import TestRDF
from vgmdb import album
from vgmdb.config import BASE_URL
from urlparse import urljoin

class TestAlbumsRDF(TestRDF):
	data_parser = lambda self,x: album.parse_album_page(x)
	outputter_type = 'album'
	def setUp(self):
		pass

	def run_ff8_tests(self, graph):
		test_count_results = {
			"select ?type where { <@base#subject> rdf:type mo:Release . }" : 1,
			"select ?type where { <@base#subject> rdf:type schema:MusicAlbum . }" : 1,
			"select ?person where { <@base#composition> mo:composer ?person . }" : 1,
			"select ?person where { <@base#performance> mo:performer ?person . }" : 8,
			"select ?person where { ?person foaf:made <@base#lyrics> . }" : 2,
			"select ?record where { <@base#subject> mo:record ?record }" : 1,
			"select ?track where { <@base#subject> mo:record ?record . ?record mo:track ?track . }" : 13
		}
		test_first_result = {
			"select ?expression where { <@base#subject> mo:publication_of ?expression . }" : "<@base#musicalexpression>",
			"select ?album where { <@base#musicalexpression> mo:published_as ?album . }" : "<@base#subject>",
			"select ?performance where { <@base#musicalexpression> mo:records ?performance . }" : "<@base#performance>",
			"select ?expression where { <@base#performance> mo:recorded_as ?expression . }" : "<@base#musicalexpression>",
			"select ?work where { <@base#performance> mo:performance_of ?work . }" : "<@base#musicalwork>",
			"select ?performance where { <@base#musicalwork> mo:performed_in ?performance . }" : "<@base#performance>",
			"select ?composed where { <@base#musicalwork> mo:composed_in ?composed . }" : "<@base#composition>",
			"select ?work where { <@base#composition> mo:produced_work ?work . }" : "<@base#musicalwork>",
			"select ?lyrics where { <@base#musicalwork> mo:lyrics ?lyrics . }" : "<@base#lyrics>",
			"select ?about where { <@base#subject> schema:about ?about . } " : "<@baseproduct/189#subject>",
			"select ?name where { ?album rdf:type mo:Release . ?album dcterms:title ?name . }" : u'FITHOS LUSEC WECOS VINOSEC: FINAL FANTASY VIII',
			"select ?catalog where { <@base#subject> mo:catalogue_number ?catalog . }" : "SSCX-10037",
			"select ?catalog where { <@base#subject> mo:other_release_of ?release . ?release mo:catalogue_number ?catalog . } order by desc(?catalog)" : "SQEX-10025",
			"select ?date where { ?album rdf:type schema:MusicAlbum . ?album dcterms:created ?date . }" : datetime.date(1999,11,20),
			"select ?name where { <@base#performance> mo:performer ?person . ?person foaf:name ?name . filter(lang(?name)='en')} order by ?name" : "Chie Sasakura",
			"select ?records where { <@base#subject> mo:record_count ?records . }" : 1,
			"select ?tracks where { <@base#subject> mo:record ?record . ?record mo:track_count ?tracks . }" : 13,
			"select ?length where { <@base#subject> mo:record ?record . ?record mo:track ?track . ?track mo:track_number \"1\"^^xsd:int . ?track schema:duration ?length . }" : "PT3:09",
			"select ?name where { <@base#subject> mo:record ?record . ?record mo:track ?track . ?track mo:track_number \"1\"^^xsd:int . ?track foaf:name ?name . filter(lang(?name)='en')}" : "Liberi Fatali",
			"select ?publisher where { <@base#subject> mo:publisher ?publisher . }" : "<@baseorg/54#subject>",
			"select ?name where { <@base#subject> schema:publisher ?publisher . ?publisher foaf:name ?name . filter(lang(?name)='en') }" : "DigiCube",
			"select ?composer where { <@base#composition> mo:composer ?composer . }" : "<@base/artist/77#subject>",
			"select ?name where { <@base#composition> mo:composer ?composer . ?composer foaf:name ?name . filter(lang(?name)='en') }" : "Nobuo Uematsu",
			"select ?composition where { <@base/artist/77#subject> foaf:made ?composition . }" : "<@base#composition>",
			"select ?rating where { <@base#subject> schema:aggregateRating ?agg . ?agg schema:ratingValue ?rating . }" : "4.47"
		}

		self.run_tests(graph, test_count_results, test_first_result)
	def test_ff8_rdfa(self):
		graph = self.load_rdfa_data('album_ff8.html')
		self.run_ff8_tests(graph)
	def test_ff8_rdf(self):
		graph = self.load_rdf_data('album_ff8.html')
		self.run_ff8_tests(graph)


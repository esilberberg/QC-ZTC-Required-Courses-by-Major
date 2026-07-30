# Zero Textbook Cost (ZTC) Required Courses at Queens College

An automated web scraping and data processing pipeline to identify which core major requirements at Queens College (CUNY) offer Zero Textbook Cost (ZTC) options.

This repository crawls the Queens College Undergraduate Bulletin, extracts required core courses for each major, cleans and parses course metadata, and cross-references those requirements against known ZTC course offerings.

## Overview
`1_get_core_courses.py` Scrapes major programs and their required core courses directly from the CUNY catalog using Selenium.

`#2_format_results` Standardize raw course strings into structured data (Class_Number and Class_Name) using Pandas.

`#3_ztc_crossreference` Flag courses in the required major lists that match the list of ZTC-designated courses as the appear in [CUNY Global Class Search](https://globalsearch.cuny.edu/CFGlobalSearchTool/search.jsp).

## What is ZTC?
[CUNY Guidelines:](https://www.cuny.edu/about/administration/offices/library-services/open-educational-resources/guidelines-for-zero-textbook-cost-course-designation/) _“Zero Textbook Cost” or ZTC is the designation used in CUNYFirst to indicate that a course does not require students enrolled in the class to purchase a textbook or required readings. Instead, students may be assigned open educational resource (OER) materials, freely available materials (which may or may not be open, but are freely accessible for students made available through a subscription or purchase by CUNY and/or your campus Library, or they may have an “open” license that authorizes their use, or it could simply be that the copyright owner has chosen to make these materials freely available on the Internet ), or a combination of these._

# ruminant

This is an open source attempt to improve upon the structure of goal management through Airtable using a Python backend to manipulate and reconstruct Airtable data. One goal of the program is to impose a hierarchical structure to goals set through Airtable, such that a given action has a clear "Why" which links to another record. Each table has its own hierarchical value, with 0 being the highest tier, or the root of the "Why"s for each goal.

Top down organization
NOTE that due to Airtable's API not supporting programmatically created fields, this program's capabilities are heavily resitricted. Should Airtable expand their API in the future to have programmatic tables and fields, then this program can easily automate that system rather than relying on a template Airtable to workwith the program.


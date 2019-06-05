  SmartDoc, a project which aim at making users to find the corresponding explanation in the srs file more quickly when thinking about the code.

  Two html file will be generated which are code.html and srs.html.

  In the srs.html, there will be links which can be in a sentence "{see ???}" to go the corresponding place in the code.html. And code.html also has links to go to srs.html for correct explanation.

   SRS will strictly follow the following format.
	@Requirement [id=rq1] [description=???]
 	Rationale  [id=ra1???] [description=???]
 	TestCase   [id=tc???] [description=???]
 	Priority   [Low/Medium/High]

  In the generated code.html file, there are not only corresponding code, but also strings in front of each block of code (with specific format), which can link to the specific location of srs.html file.

?Correspondingly, in the srs.html file can also jump to the corresponding location of the code.html file. At the bottom of the srs.html, there are two tracable matrix.

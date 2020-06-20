# UniversityDirectoryScraperV2
UniversityDirectoryScraper rewritten and expanded with Selenium.

This script contains a lot of functionality, albeit with some of it obscured due to an agreement with the university IT department.

**Functions**
<ul>
  <li>scraper() - Following login, downloads names, emails, and profile picture links from directory.</li>
  <li>exportNamesAndEmails() - Takes the file that contains the names, emails, and photo links and separates out the names and emails, saving them in separate files. </li>
  <li>downloadImages() - Takes the photo links and uses them to download images to local machine.</li>
  <li>newlinetocommalist() - Converts file containing photos to comma separated list (I needed this for something with JavaScript I think?).</li>
  <li>facecomparison() - Takes in photo and compares it against university database, increasing similarity strictness until only one result is left.</li>
  <li>create_encodings() - Creates the face encodings so you don't have to generate them whenever you compare a face (super resource intensive).</li>
  <li>findID() - Iterates through all possible ID numbers, converts those numbers to md5 hash values, and compares those hash values to the photo URLs already acquired to find photos that were not listed on the internal directory.</li>
</ul>

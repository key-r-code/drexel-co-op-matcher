# drexel-co-op-matcher

```

                              ______________                               
                        ,===:'.,            `-._                           
                             `:.`---.__         `-._                       
                               `:.     `--.         `.                     
                                 \.        `.         `.                   
                         (,,(,    \.         `.   ____,-`.,                
                      (,'     `/   \.   ,--.___`.'                         
                  ,  ,'  ,--.  `,   \.;'         `                         
                   `{D, {    \  :    \;                                    
                     V,,'    /  /    //                                    
                     j;;    /  ,' ,-//.    ,---.      ,                    
                     \;'   /  ,' /  _  \  /  _  \   ,'/                    
                           \   `'  / \  `'  / \  `.' /                     
                            `.___,'   `.__,'   `.__,'  

 ```

 

## About

Ever get tired of manually scrolling through all the co-op postings on DrexelOne all within one week? Now you don't have to!

This project aims to automate finding all those co-ops you might be best suited for using an LLM pipeline. 

## How it works

1. Web Scraping

- Uses Selenium to log into DrexelOne and scrape available job postings.
- Saves all the static HTML pages in a directory.
- Uses BeautifulSoup to parse all the scraping into a single json file.

2. LLM pipeline

- Chunks and 


## Usage

### Scraping jobs from Drexel Banner

### LLM pipeline



### TO DO:

#### dragonScraper.py

- Add pagination handling
- Add upcoming co-op postings and previously applied co-ops 
- Replace all time.sleep() calls with self.wait.until

#### LLM-pipeline

- Add a geminiPipeline class
- Find optimal chunk_size and chunk_overlap


#### CLI App

- Add API key handling
- Add A/B/C round navigation
- Add major navigation



## Contributions

Project may stop working at any time, contributions are welcome! To contribute:

1. Fork the repository.

2. Create a new branch (git checkout -b feature/my-new-feature).

3. Make your changes.

4. Commit your changes (git commit -am 'Add new feature').

5. Push to the branch (git push origin feature/my-new-feature).

6. Create a pull request.
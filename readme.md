# Applicant Tracking System (ATS) 

[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)

<!-- [![PyPI version](https://badge.fury.io/py/Django.svg)](https://badge.fury.io/py/Django)
[![CI](https://github.com/athityakumar/colorls/actions/workflows/ruby.yml/badge.svg)](https://github.com/athityakumar/colorls/actions/workflows/ruby.yml) -->

One of the core components in the integrated architecture of the Recruitment NWoW/process re-engineering, **Applicant Tracking System (ATS)** is a web-based application envisioned to serve as a one-stop center for recruitment activities within DS department. The app is designed to handle the tracking of applicants and various automations associated with routine processes throughout the application

The app is powered by **[Django](https://docs.djangoproject.com/en/4.2/intro/) framework** (backend) along with traditional **HTML/CSS/JavaScript** stack in the frontend. Therefore, intermediate knowledge of Python & Django framework may be an advantage to work with the source code.

This *readme.md* aims to provide an overview of the system, installation and build steps, as well as the documentation of the source code as part of the project handover.  
<br>

# Table of contents
<details open>
<summary>Enlarge the details for the complete TOC</summary>

- [Applicant Tracking System (ATS)](#applicant-tracking-system-ats)
- [Table of contents](#table-of-contents)
- [Local Installation](#local-installation)
- [Overview of ATS](#overview-of-ats)
  - [Candidate Browse/List Page](#candidate-browselist-page)
  - [Stage Page](#stage-page)
    - [Initial Screening](#initial-screening)
    - [Preasssement](#preasssement)
- [Updating](#updating)
- [Uninstallation](#uninstallation)
- [Contributing](#contributing)
- [License](#license)
</details>
<br>

# Local Installation

[(Back to top)](#table-of-contents)

*Note that this guideline uses **git bash** as the CLI erminal to execute commands*

1. `git clone` the project repo into any preferred directory in your local environment
2. Open CLI and navigate to the project directory:
    ```sh
    # navigate to project directory
    cd path/to/directory 
    ```
3. Set-up a virtual environment for the project repository. There are multiple ways to achieve this. If you are familiar with *Conda* or any other tools, you can proceed with creating an environment in Conda. Otherwise, you may follow the below steps to create an environment using ***Venv***
    
    1. Install Python (preferably, version >= 3.9)
    2. Open the project directory in CLI (make sure the CLI is navigated to the project's root directory) and execute the following commands:
        
        ```sh
        cd path/to/directory
        
        # create environment
        python -m venv .venv
        
        # activate environment (cmd)
        .venv/scripts/activate
        
        # activate environment (git bash)
        source .venv/scripts/activate
        ```

4. Install the required dependencies as in the `requirements.txt` file

    ```sh
    pip install -r requirements.txt
    ```

5. Now that the project environment is ready, it's time to initiate the database creation and run the development server.

    Run the following commands to create (and migrate) database:

    ```sh
    cd recruitment

    # Create any new database migrations
    python manage.py makemigrations

    # Commit the migrations into the database (db.sqlite)
    python manage.py migrate
    ```

6. Finally, run the development server as follows:
    ```sh
    python manage.py runserver
    ```

    Access the ATS via the localhost url e.g. `http://localhost:8000/` 

<br>

# Overview of ATS

[(Back to top)](#table-of-contents)

At this point, you should be able to access the ATS running in the development server. In short, the `runserver` command allows the developers to test and debug their app by running in the local server. Every changes made to the app will be imediately reflected in the browser wihout the need to set up a production server.

As of now, ATS entails 5 functioning web pages dedicated for the full tracking functionalities of the candidates' application. The following explanations briefly describe their respective purpose and key components embedded in the section.

## Candidate Browse/List Page

<details>

<summary>Expand/collapse details</summary>
<br>

As the name suggests, this page is initially dedicated to displaying the overview/summary of all received candidates for DS department. Nevertheless, it has been gradually developed to embed CRUD functionalities to modify the application status of the candidates. The intention is that the hiring manager/execs can instantly manipulate the status/information of the large volume of candidates from a single view.

The following numbered list explain the key components in the browse page:

1. **Upload Resume** button:

    Upon clicking the button, a modal dedicated to uploading resume(s) will appear that includes;  
    
      * `file input` field that accepts multiple file uploads
      * `source` dropdown field to specify the source of resumes
      * `upload` button to upload the resumes into the database. 
      * `upload and parse` button which alternatively redirects the user to *Parse Resume* modal dedicated to uploading and parsing the resumes in one continuous flow.

    <br>
   
2. **Parse Resume** button:
   
    Upon clicking the button, a modal dedicated to parsing new (uploaded) resume(s) will appear which includes;
    
    * **Count of resumes** to be parsed
    * Parser configurations input consisting of `job title` and `job description` fields to match the candidates with specific applied position
    * `Parse Resumes` button to trigger the resume parsing process
    * `Save configuration` checkbox to save the newly edited `job title` and `job description` when clicking the `Parse Resumes` button
    
    <br>

3. **GPT Score Threshold** Filter:

    Each candidate is associated with a certain value of **GPT score** which is derived from the resume parsing process. The `threshold` sets the minimum value/percentage for the score that which filters out candidates in the table that meet the condition. The `toggle` either enables or disable the GPT Score threshold filter.

4. **Source** Filter: Filters out the candidates that are received from a selected source

5. Table Filters: Filters out the candidates based on the selected value in specific column(s)

    ***For `Received Date` column, the `date input` sets the *starting value* of the range , which means the filtered received date will be from *inputted date --> current date*

6. **Status** dropdowns: The users can utilize the `dropdown` to update the application status for each applicant. 
    
    *Technical note: Upon the value change of the dropdown, the relevant event sends an API call in the background to the server to update the status of the stage. Then, the table is refreshed to reflect the latest change.*

</details>

## Stage Page

There are **three stages** that the candidate must undergo throughout the application process, as depicted by the process flow below.

<p style="font-size:16px;font-weight:600;">Initial Screening ➡ Preassessment (HackerRank) ➡ Competency-based Interview (CBI) ➡ *Joining </p>

### Initial Screening

The initial screening stage involves 2 phases. 

In the first phase, the hiring manager (HM) reviews and assesses the information of the candidates (extracted from the resume). Once the decision is made, HM updates the `Hiring Manager Screening` status whether to proceed or reject the candidate. If `status = proceed`, the process continues to the 2nd phase, otherwise (`status = proceed`) the application is not continued.

The second phase requires the decision from other managers in the `DS Lead Screening` section whether to proceed with the candidate. As this part of the system is a work-in-progress, the current view is intended for the hiring manager only. Ideally, the view of this section for other managers should not display include others' vote and only diplay the only user's vote. In this case, the other managers can access the  to cast a vote. In the end, a majority vote is implemented to determine the status of the applicant, in which the status is reflected in the `Final Decision` section.

### Preasssement

There are three phases involved in the preassessment (initially called Prescreening) stage, as illustrated by the below flow 



ATS wil handle certain automations triggered by the user, as follows


# Updating

[(Back to top)](#table-of-contents)

Want to update to the latest version of `colorls`?

```sh
gem update colorls
```

# Uninstallation

[(Back to top)](#table-of-contents)

Want to uninstall and revert back to the old style? No issues (sob). Please feel free to open an issue regarding how we can enhance `colorls`.

```sh
gem uninstall colorls
```

# Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. :tada:

# License

[(Back to top)](#table-of-contents)


The MIT License (MIT) 2017 - [Athitya Kumar](https://github.com/athityakumar/). Please have a look at the [LICENSE.md](LICENSE.md) for more details.

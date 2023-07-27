#Django reddit
Reddit clone written in python using django web framework and twitter's bootstrap.

[![Build Status](https://travis-ci.org/Nikola-K/django_reddit.svg)](https://travis-ci.org/Nikola-K/django_reddit) [![Coverage Status](https://coveralls.io/repos/Nikola-K/django_reddit/badge.svg?branch=master&service=github)](https://coveralls.io/github/Nikola-K/django_reddit?branch=master)

#Screenshots

![desktop_frontpage](_screenshots/desktop_frontpage 2015-06-22.jpg?raw=true)

![desktop_submission](_screenshots/desktop_submission 2015-06-22.jpg?raw=true)

![profile_view](_screenshots/profile_view 2015-06-24.png)

![profile_edit](_screenshots/profile_edit 2015-06-24.png)

Fully responsive:

![mobile_frontpage](_screenshots/mobile_frontpage 2015-06-22.png?raw=true)

![mobile_submit](_screenshots/mobile_submit 2015-06-22.png?raw=true)

![mobile_thread](_screenshots/mobile_thread 2015-06-22.png?raw=true)

#Getting up and running

The project is python 3 only.

The steps below will get you up and running with a local development environment. We assume you have the following installed:

    pip
    virtualenv
    
First make sure to create and activate a virtualenv, then open a terminal at the project root and install the requirements for local development:

    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py syncdb
    $ python manage.py runserver
    
For the time being there is no separate production specific settings because the project is not yet production ready.

#Deployment

* TODO: Write here how to deploy

#License

    Copyright 2016 Nikola Kovacevic <nikolak@outlook.com>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

# cm1_python_test
For candidates interested in working for cm1
Please fork this repo.  Done.

<h3> Main Test </h3>
Please open CM1_DevQuickTest_Question.ipynb for the main tasks. Make a copy of the notebook rather than working on the main one.
<u>Deliverables: </u> The link for your own colab workbook

<h3>Django Test Instruction</h3>

Hi there! You are going to make edits on a Django project. The Django project is a super simple version of Reddit. Note that the repo uses terminology that differs from Reddit terminology. Clone this repo (https://github.com/nikolak/django_reddit) and complete the following tasks:

1. Make it work.
   There are a couple bugs in the repo. Depending on your version, bugs are very likely to occur. We expect you to fix these bugs and make the original code run.
   <u> Deliverables:</u> Make a post with your full name and the date (Jul 04, 2023) or (MMM DD, YYYY) format and send over the screenshot.
   ![example image](https://drive.google.com/uc?id=147DRoB2dsmuXi_ABcEapiw-RpWvJoM0m)

2. For submissions that have URL, the code will automatically direct you to the URL rather than the submissions detail page. We are going to change it. When a user clicks on the submission/post from the home page, it will direct them to the detailed submission page (please find the right views.py function). If a submission has a URL, we will just display the URL as an additional line instead.
   <u> Deliverables:</u> You are going to make two posts, one with a URL and the other one without URL and send over the screenshot.
   ![example image](https://drive.google.com/uc?id=13TPEmHFWPcXML09gv4GSPOAYUHSx-RLv)

3. Let's add some additional information: submissions and comments on the user profile.
   <u> Deliverables:</u>: Make a couple of posts after registering yourself and take a screenshot of your profile with the list of comments and submissions.
   ![example image](https://drive.google.com/uc?id=1MqkgpmH0VG-_B-0Eq9Bb0Ylo4Pb0MUOZ)

4. Let's add an "Edit" button on the comment page that allows the right user to edit his own submissions.
   <u> Deliverables: </u>: Take two screenshots of the new comments page with the functioning "edit" bottom. First screenshot shows the submission and the second screenshot shows the SAME submission (with the same ID) but with edited content.

   Before:
   ![example image](https://drive.google.com/uc?id=16BUlkbCDKryD6g6dBZ4D5xNszgiKhfxD)

   After:
   ![example image](https://drive.google.com/uc?id=1VUzEJd9h8o6ppJO6JLR1f_1fEXo3gFb7)

5. Finally, please upload a youtube or loom video going over a live demo with the above tasks.
   
![profile_update](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/5e01bb69-8c2f-4faa-8d50-566c11b54cb3)


![submissions_withou![without_edit_button](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/aae08573-ddc3-442b-a6ba-758d2b559b16)
t_url](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/49e86f39-09c7-4eb7-9aed-38320e93cb57)

![Submissions _with_edit_button](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/d3e64428-88eb-49b1-98cc-a8589c4e6322)

![submissions and comments on the user profile2](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/1312195c-953f-4aaf-a826-1338ee6a723e)
![Submissions_with_url](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/9c2cf9b6-54f6-478c-bd1d-2ee8782c81e4)

![profile_edit 2015-06-24](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/e3586424-eff0-4746-bc4c-0fd7c2eaefb3)

![submissions and comments on the user profile1](https://github.com/ONJoseph/django_reddit_clone/assets/60672480/aa87c5ea-9501-404e-b7a9-02d871516a0b)

Loom Video Link: https://www.loom.com/share/ade2f025929840808c2e0fd342b67f0c 

   <h3>Once you finish, please reach out with your repo link. You can also email me at louisa@communityone.io</h3>

   

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PDFDocument1,Skill,Project,SuggestedTechnology
from django.http import FileResponse, JsonResponse
from django.core.files import File
from wsgiref.util import FileWrapper
import os
import PyPDF2
from PyPDF2 import PdfReader
import spacy
import re
from django.core.mail import send_mail
from .models import UserAccount
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ScrapedContent
import requests
from bs4 import BeautifulSoup




def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # The user is valid, so log them in
            login(request, user)
            # Redirect to a success page or wherever you want
            return redirect('dashboard')
        else:
            # Authentication failed, handle it accordingly
            # For example, show an error message
            error = "Invalid login credentials."
            return render(request, 'index.html', {'error': error, })

    return render(request, 'index.html')




def register(request):
    if request.method == 'POST':
        cname = request.POST['name']
        cemail = request.POST['email']
        cusername = request.POST['username']
        cpassword = request.POST['password']
        user = User.objects.create_user(username=cusername, password=cpassword, email=cemail,first_name=cname)
        #myuser = User.objects.create_user(name, email, username, password)
        #myuser.is_active = False
        user.save()
        messages.success(request, "Your Account has been created succesfully!!")
        return redirect('index')
                
    return render(request, "pages-register.html")

def dashboard(request):
    return render(request,'Dashboard.html')

def faq(request):
    return render(request,'pages-faq.html')

def contact(request):
    return render(request,'pages-contact.html')

def upload_pdf1(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            # Create a PDFDocument object and save the uploaded file
            pdf_document = PDFDocument1(file=pdf_file)
            pdf_document.save()

            # Extract text from the PDF
            text = ""
            pdf_file = pdf_document.file.path
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            

            #text = ' '.join(re.findall(r'\b\w+\b', text))
            #cleaned_text = re.sub(r'[^a-zA-Z]', '', text)
            text=text.lower()
            #print(text)
            # Load the English NLP model from spaCy
            nlp = spacy.load("en_core_web_sm")

            # Assuming you have the extracted text stored in a variable named 'text'
            doc = nlp(text)

            # Tokenization
            tokens = [token.text for token in doc]
            # Specialization determination
            specialization = determine_specialization(doc)

            # Keyword extraction
            keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

            # Save the extracted text in the database
            pdf_document.extracted_text = text
            pdf_document.save()
            #print("******************************")
            #print(specialization)

            try:
                skill = Skill.objects.get(name=specialization)
                projects = Project.objects.filter(skill=skill)
                technologies = SuggestedTechnology.objects.filter(project__in=projects)
            except Skill.DoesNotExist:
                skill = None
                projects = []
                technologies = []
            
        
            context = {
                'specialization':specialization,
                'skill': skill,
                'projects': projects,
                'technologies': technologies,
            }
            #print(skill,projects,technologies)
            return render(request,'dashboard.html',context)
            #return HttpResponse("Here's") # Redirect to a success page
            #return render(request,'suggested_tech.html',{"area_specialization":specialization})
    else:
        return render(request, 'dashboard.html')  # Render the upload form
# Add a URL pattern for the view in your urls.py
# You'll also need to create an HTML template for the upload form.


def determine_specialization(doc):
    specialization = "Unknown"  # Default specialization
    try:
        # Define a list of keywords or key phrases related to different specializations
        web_dev_keywords = ["web development", "full stack", "front-end", "back-end", "web design","react","java","django","nodejs","mysql","mongodb","html","css","javascript","bootstrap","tailwind","figma"]
        data_science_keywords = ["data science", "machine learning", "data analysis", "AI","R","sas","matlap","hadoop"]
        software_eng_keywords = ["software engineering", "coding", "programming", "software development","linux"]
        
      
        # Check for the presence of keywords in the resume text
        text = doc.text.lower()  # Convert text to lowercase for case-insensitive matching
        if any(keyword in text for keyword in data_science_keywords):
            specialization = "Data Science"
        elif any(keyword in text for keyword in web_dev_keywords):
            specialization = "Web Development"
        elif any(keyword in text for keyword in software_eng_keywords):
            specialization = "Software Engineering"
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        specialization = "Error"  # Handle the error
    return specialization


def Dashboard(request):
    return render(request,"Dashboard.html")

def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct the email message
        email_message = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'

        # Send the email
        send_mail(
            subject,
            email_message,
            email,  # Use the sender's email as the "from" address
            ['junitcp21@gmail.com'],  # Replace with admin's email
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email sent successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)

from django.shortcuts import render, redirect

def create_account(request):
    return render(request, 'index.html')

def fgt_pwd(request):
    return render(request,'forgot-password.html')


def scrape_website(request):
    if request.method=='POST':
        c_url = request.POST.get('c_url')
        url = c_url  # Replace with the URL of the website you want to scrape
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find and extract the title of the website
            
            # Find and extract the title of the website
            title = soup.find('title').text

            # Find and extract all div elements
            divs = [div.get_text() for div in soup.find_all('div')]

            # Find and extract all headings (h1, h2, h3, etc.)
            #headings = [heading.get_text() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

            # Find and extract all paragraphs (p tags)
            paragraphs = [p.get_text() for p in soup.find_all('p')]

            # Find and extract all lists (ul and ol elements)
            lists = [ul.get_text() for ul in soup.find_all(['ul', 'ol'])]

            #print(title)
            #print(divs) li
            #print(headings) li
            #print(paragraphs) li
            #print(lists) li
            result_list=[]
            result_list.append(divs)
            
            result_list.append(paragraphs)
            result_list.append(lists)

            string_result = ', '.join(str(item) for item in result_list)
            scraped_content = ScrapedContent(content=string_result)
            scraped_content.save()
            #print(string_result)
            modified_text = string_result.replace('\n', ' ')
            print(modified_text)
            
            specialization = "Unknown"  # Default specialization
            try:
                # Define a list of keywords or key phrases related to different specializations
                web_dev_keywords = ["web development", "full stack", "front-end", "back-end", "web design","react","java","django","nodejs","mysql","mongodb","html","css","javascript","bootstrap","tailwind","figma"]
                data_science_keywords = ["data science", "machine learning", "data analysis", "AI","R","sas","matlap","hadoop"]
                software_eng_keywords = ["software engineering", "coding", "programming", "software development","linux"]
                
                # Check for the presence of keywords in the resume text
                text =modified_text.lower()  # Convert text to lowercase for case-insensitive matching
                if any(keyword in modified_text for keyword in data_science_keywords):
                    specialization = "Data Science"
                elif any(keyword in modified_text for keyword in web_dev_keywords):
                    specialization = "Web Development"
                elif any(keyword in modified_text for keyword in software_eng_keywords):
                    specialization = "Software Engineering"
            except Exception as e:
                print(f"Error processing resume: {str(e)}")
                specialization = "Error"  # Handle the error

            print(specialization)
        
            try:
                skill = Skill.objects.get(name=specialization)
                projects = Project.objects.filter(skill=skill)
                technologies = SuggestedTechnology.objects.filter(project__in=projects)
            except Skill.DoesNotExist:
                skill = None
                projects = []
                technologies = []
                
            context = {
                    'specialization':specialization,
                    'skill': skill,
                    'projects': projects,
                    'technologies': technologies,
            }
            return render(request,'scraped_data.html',context)
        else:
            return render(request, 'Dashboard.html', {'message': 'Failed to fetch data from the website'})
    else:
        return render(request, 'Dashboard.html', {'message': 'Failed to fetch data from the website'})


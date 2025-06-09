#README with setup instructions and sample cURL or Postman requests
# Fitness Studio API
# This API allows you to manage fitness classes, clients, and bookings.     
#
# ## Setup Instructions     
# 1. Clone the repository:
#    ```bash
#    git clone                      

#    ```
# 2. Navigate to the project directory:             
#    ```bash
#    cd fitness_studio
#    ```    
# 3. Install the required packages:
#    ```bash
#    pip install -r requirements.txt
#    ```
# 4. Run the migrations:
#    ```bash    
#    python manage.py migrate
#    ```
# 5. Create a superuser to access the admin panel:
#    ```bash                

# 6. Setting up Seed Data
#    ```bash    
#     cd scripts
#    python seed_data.py
#    cd ..
#    ```


#    python manage.py createsuperuser
#    ```
# 7. Start the development server:      
#    ```bash            
#    python manage.py runserver
#    ```            

# 8. Access the admin panel at `http://localhost:8000/admin/`    

# ## Sample cURL Requests               
# ### Look at available Fitness classes
# ```cmd       
# curl -H "Accept: application/json" http://localhost:8000/fitness_studio/classes
# ```

# ### Book a Fitness Class
# ```cmd      
# curl -X POST http://localhost:8000/fitness_studio/book -d "class_id=1" -d "client_name=Test User" -d "client_email=test@test.com"
# ```

# ### See Bookings
# ```cmd      
# curl -H "Accept: application/json" http://localhost:8000/fitness_studio/bookings?client_email=test@test.com
# ```

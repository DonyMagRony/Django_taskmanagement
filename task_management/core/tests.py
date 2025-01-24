from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .models import User, Project, Category, Priority, Task


class ViewSetTests(APITestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username="admin", password="admin123", role="admin", email="admin@test.com"
        )
        self.manager_user = User.objects.create_user(
            username="manager", password="manager123", role="manager", email="manager@test.com"
        )
        self.employee_user = User.objects.create_user(
            username="employee", password="employee123", role="employee", email="employee@test.com"
        )

        # Create tokens for users
        self.admin_token = str(AccessToken.for_user(self.admin_user))
        self.manager_token = str(AccessToken.for_user(self.manager_user))
        self.employee_token = str(AccessToken.for_user(self.employee_user))

        # Create sample data with `start_date` populated
        self.project = Project.objects.create(
            name="Test Project", 
            description="A sample project", 
            start_date=date.today(), # Ensure start_date is provided
            end_date="2025-12-31",
        )
        self.category = Category.objects.create(name="Sample Category")
        self.priority = Priority.objects.create(level="High Priority")


    def test_user_viewset_admin_access(self):
        # Admin should be able to access UserViewSet
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/users/")  # Replace with your UserViewSet endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_viewset_manager_access_denied(self):
        # Manager should not have access to UserViewSet
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_viewset_manager_access(self):
        # Manager should be able to access ProjectViewSet
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.get("/api/projects/")  # Replace with your ProjectViewSet endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_viewset_employee_access(self):
        # Employee should be able to access TaskViewSet
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.employee_token}")
        response = self.client.get("/api/tasks/")  # Replace with your TaskViewSet endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_creation_as_employee(self):
        # Employee should be able to create a task
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.employee_token}")
        data = {
            "title": "New Task",
            "description": "Task description",
            "project": self.project.id,
            "priority": self.priority.id,
            "category": self.category.id,
        }
        response = self.client.post("/api/tasks/", data)  # Replace with your TaskViewSet endpoint
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_creation_as_unauthorized_user(self):
        # Without authorization, task creation should fail
        data = {
            "title": "Unauthorized Task",
            "description": "This should fail",
            "project": self.project.id,
            "priority": self.priority.id,
            "category": self.category.id,
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


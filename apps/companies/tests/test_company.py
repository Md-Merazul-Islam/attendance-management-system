from django.test import TestCase
from apps.companies.models import Company
from django.utils import timezone
import uuid


class CompanyModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.company = Company.objects.create(
            company_name="Test Company",
            location="Dhaka, Bangladesh"
        )
    
    def test_company_creation(self):
        """Test that a company can be created successfully"""
        self.assertIsNotNone(self.company)
        self.assertEqual(self.company.company_name, "Test Company")
        self.assertEqual(self.company.location, "Dhaka, Bangladesh")
    
    def test_company_uid_generation(self):
        """Test that UID is automatically generated"""
        self.assertIsNotNone(self.company.uid)
        self.assertIsInstance(self.company.uid, uuid.UUID)
    
    def test_company_uid_uniqueness(self):
        """Test that each company has a unique UID"""
        company2 = Company.objects.create(
            company_name="Another Company",
            location="Chittagong"
        )
        self.assertNotEqual(self.company.uid, company2.uid)
    
    def test_company_created_at_auto_set(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.company.created_at)
        self.assertLessEqual(
            self.company.created_at, 
            timezone.now()
        )
    
    def test_company_str_representation(self):
        """Test the string representation of company"""
        self.assertEqual(str(self.company), "Test Company")
    
    def test_company_with_blank_location(self):
        """Test company creation with blank location"""
        company = Company.objects.create(
            company_name="No Location Company",
            location=""
        )
        self.assertEqual(company.location, "")
    
    def test_company_with_null_location(self):
        """Test company creation with null location"""
        company = Company.objects.create(
            company_name="Null Location Company",
            location=None
        )
        self.assertIsNone(company.location)
    
    def test_company_name_max_length(self):
        """Test that company name respects max_length"""
        max_length = Company._meta.get_field('company_name').max_length
        self.assertEqual(max_length, 255)
    
    def test_company_update(self):
        """Test updating company details"""
        self.company.company_name = "Updated Company"
        self.company.location = "Sylhet"
        self.company.save()
        
        updated_company = Company.objects.get(uid=self.company.uid)
        self.assertEqual(updated_company.company_name, "Updated Company")
        self.assertEqual(updated_company.location, "Sylhet")
    
    def test_company_deletion(self):
        """Test deleting a company"""
        company_uid = self.company.uid
        self.company.delete()
        
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(uid=company_uid)
    
    def test_multiple_companies_creation(self):
        """Test creating multiple companies"""
        companies = [
            Company.objects.create(
                company_name=f"Company {i}",
                location=f"Location {i}"
            ) for i in range(5)
        ]
        
        self.assertEqual(Company.objects.count(), 6)  # 5 + 1 from setUp
    
    def test_company_query_by_name(self):
        """Test querying company by name"""
        company = Company.objects.get(company_name="Test Company")
        self.assertEqual(company.uid, self.company.uid)
    
    def test_company_query_by_uid(self):
        """Test querying company by UID"""
        company = Company.objects.get(uid=self.company.uid)
        self.assertEqual(company.company_name, "Test Company")
    
    def test_company_filter_by_location(self):
        """Test filtering companies by location"""
        Company.objects.create(
            company_name="Company 2",
            location="Dhaka, Bangladesh"
        )
        Company.objects.create(
            company_name="Company 3",
            location="Chittagong"
        )
        
        dhaka_companies = Company.objects.filter(location="Dhaka, Bangladesh")
        self.assertEqual(dhaka_companies.count(), 2)
    
    def test_company_ordering(self):
        """Test default ordering (if any)"""
        company1 = Company.objects.create(company_name="A Company")
        company2 = Company.objects.create(company_name="Z Company")
        
        companies = list(Company.objects.all())
        # Since no ordering is defined, just check all exist
        self.assertEqual(len(companies), 3)  # 1 from setUp + 2 new
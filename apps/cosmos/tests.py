from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.cosmos.models import DataModel, Taxonomy, Results, SubSample, RootSample
from django.contrib.auth import get_user_model

class CosmosAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.user.email_verified = True
        self.user.save()

        # Perform login
        url = reverse('users_api:login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Extract tokens
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

        # Set the access token in the client's credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Create test data
        self.root_sample = RootSample.objects.create(name="Test Root Sample")
        self.sub_sample = SubSample.objects.create(
            name="Test Sub Sample", root_sample=self.root_sample
        )
        self.results = Results.objects.create(
            name="Bacteria", sub_sample=self.sub_sample
        )
        self.taxonomy = Taxonomy.objects.create(
            name="Test Taxonomy", result_of=self.results
        )
        self.data_model = DataModel.objects.create(
            name="Test Model",
            taxonomy=self.taxonomy,
            result_of=self.results,
            tax_id=12345,
            relative_abundance=0.5,
            file_name="test_file.txt"
        )

    def test_root_samples_crud(self):
        url = reverse("cosmos_api:RootSampleViewSet-list")

        # Test CREATE
        response = self.client.post(url, {"name": "New RootSample"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test READ (list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # Test READ (detail)
        detail_url = reverse("cosmos_api:RootSampleViewSet-detail", kwargs={"pk": self.root_sample.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Root Sample")

        # Test UPDATE
        response = self.client.put(detail_url, {"name": "Updated RootSample"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RootSample.objects.get(pk=self.root_sample.pk).name, "Updated RootSample")

        # Test PATCH
        response = self.client.patch(detail_url, {"name": "Patched RootSample"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RootSample.objects.get(pk=self.root_sample.pk).name, "Patched RootSample")

        # Test DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RootSample.objects.filter(pk=self.root_sample.pk).exists())

    def test_sub_samples_crud(self):
        url = reverse("cosmos_api:SubSampleViewSet-list")

        # Test CREATE
        response = self.client.post(url, {"name": "New SubSample", "root_sample": self.root_sample.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test READ (list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # Test READ (detail)
        detail_url = reverse("cosmos_api:SubSampleViewSet-detail", kwargs={"pk": self.sub_sample.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Sub Sample")

        # Test UPDATE
        response = self.client.put(detail_url, {"name": "Updated SubSample", "root_sample": self.root_sample.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubSample.objects.get(pk=self.sub_sample.pk).name, "Updated SubSample")

        # Test PATCH
        response = self.client.patch(detail_url, {"name": "Patched SubSample"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubSample.objects.get(pk=self.sub_sample.pk).name, "Patched SubSample")

        # Test DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SubSample.objects.filter(pk=self.sub_sample.pk).exists())

    def test_results_crud(self):
        url = reverse("cosmos_api:ResultsViewSet-list")

        # Test CREATE
        response = self.client.post(url, {"name": "New Result", "sub_sample": self.sub_sample.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test READ (list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # Test READ (detail)
        detail_url = reverse("cosmos_api:ResultsViewSet-detail", kwargs={"pk": self.results.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Bacteria")

        # Test UPDATE
        response = self.client.put(detail_url, {"name": "Updated Result", "sub_sample": self.sub_sample.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Results.objects.get(pk=self.results.pk).name, "Updated Result")

        # Test PATCH
        response = self.client.patch(detail_url, {"name": "Patched Result"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Results.objects.get(pk=self.results.pk).name, "Patched Result")

        # Test DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Results.objects.filter(pk=self.results.pk).exists())

    def test_taxonomy_crud(self):
        url = reverse("cosmos_api:TaxonomyViewSet-list")

        # Test CREATE
        response = self.client.post(url, {"name": "New Taxonomy", "result_of": self.results.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test READ (list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        # Test READ (detail)
        detail_url = reverse("cosmos_api:TaxonomyViewSet-detail", kwargs={"pk": self.taxonomy.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Taxonomy")

        # Test UPDATE
        response = self.client.put(detail_url, {"name": "Updated Taxonomy", "result_of": self.results.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Taxonomy.objects.get(pk=self.taxonomy.pk).name, "Updated Taxonomy")

        # Test PATCH
        response = self.client.patch(detail_url, {"name": "Patched Taxonomy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Taxonomy.objects.get(pk=self.taxonomy.pk).name, "Patched Taxonomy")

        # Test DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Taxonomy.objects.filter(pk=self.taxonomy.pk).exists())

    def test_data_model_crud(self):
        url = reverse("cosmos_api:DataModelViewSet-list")

        # Test CREATE
        response = self.client.post(url, {
            "name": "New Model",
            "taxonomy": self.taxonomy.pk,
            "result_of": self.results.pk,
            "tax_id": 54321,
            "relative_abundance": 0.7,
            "file_name": "new_file.txt"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test READ (list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Including the one created in setUp
        self.assertEqual(len(response.data['results']), 2)

        # Test READ (detail)
        detail_url = reverse("cosmos_api:DataModelViewSet-detail", kwargs={"pk": self.data_model.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Model")

        # Test UPDATE
        response = self.client.put(detail_url, {"name": "Updated Model", "taxonomy": self.taxonomy.pk, "result_of": self.results.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DataModel.objects.get(pk=self.data_model.pk).name, "Updated Model")

        # Test PATCH
        response = self.client.patch(detail_url, {"name": "Patched Model"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DataModel.objects.get(pk=self.data_model.pk).name, "Patched Model")

        # Test DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DataModel.objects.filter(pk=self.data_model.pk).exists())

    def test_data_model_filters(self):
        url = reverse("cosmos_api:DataModelViewSet-list")

        # Test filter by name
        response = self.client.get(url, {"name": "Test Model"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by tax_id
        response = self.client.get(url, {"tax_id": "12345"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by relative_abundance_range
        response = self.client.get(url, {"relative_abundance_range": "0.4,0.6"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by file_name
        response = self.client.get(url, {"file_name": "test_file"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by result_of
        response = self.client.get(url, {"result_of": self.results.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by taxonomy
        response = self.client.get(url, {"taxonomy": self.taxonomy.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by root_sample
        response = self.client.get(url, {"root_sample": self.root_sample.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

        # Test filter by sub_sample
        response = self.client.get(url, {"sub_sample": self.sub_sample.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

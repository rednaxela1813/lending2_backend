import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from properties.models import Property, PropertyImage



@pytest.mark.django_db
def test_create_property():
    prop = Property.objects.create(
        name = "Test Property",
        type = "office",
        description = "Test description",
        location = "Test location"
        
    )
    
    assert prop.name == "Test Property"
    assert prop.type == "office"
    assert prop.description == "Test description"
    
    
@pytest.mark.django_db
def test_create_property_image():
    prop = Property.objects.create(
        name="Test Billboard",
        type="billboard",
        description="Big one",
        location="Highway 66"
    )

    image = PropertyImage.objects.create(
        property=prop,
        image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
        description="Main billboard image"
    )

    assert image.property == prop
    assert image.description == "Main billboard image"
    assert str(image) == f"Изображение для {prop.name}"
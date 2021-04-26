from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=20, help_text='Name')
    description = models.CharField(max_length=200, help_text='Description')

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.CharField(max_length=20, help_text='Name')        
    make = models.ForeignKey(CarMake, on_delete=models.SET_NULL, null=True)

    dealer_id = models.IntegerField(help_text='Dealer Id')
    
    TYPE_NAMES = (('sedan', 'Sedan'), ('suv', 'SUV'), ('wagon','Wagon'))
    type_name = models.CharField(
        max_length=10,
        choices=TYPE_NAMES,
        blank=True,
        default='sedan',
        help_text='Car Type',
    )

    year = models.DateField()
    
    def __str__(self):
        return self.name + self.type_name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

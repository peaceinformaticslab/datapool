from django.db import models
from django.contrib.auth.models import User
from ordered_model.models import OrderedModel
#from parselib.xmlParse import xmlImport
#from parselib.csvParse import CsvImport

# Create your models here.

class DataConnection(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	host = models.URLField()
	port = models.IntegerField(default=2424)
	name = models.CharField(max_length=30)
	
	def __unicode__(self,):
		return "%s - %s" % (self.name, self.host)


class DataSourceFlags(models.Model):
	name = models.CharField(max_length=30)
	description = models.TextField()

class DataSource(models.Model):

	DATATYPECHOICE = (
	    (0, 'CSV'),
	    (1, 'XML'),
	    (2, 'JSON'),
	    (3,'FROM QUERY')
	)

	OLDDATACHOICE = (
	    (0, 'REMOVE'),
	    (1, 'APPEND'),
	    (2, 'OVERWRITE'),
	)

	name = models.CharField(max_length=30)
	url = models.URLField(null=True)
	owner = models.ForeignKey(User)
	prefix = models.CharField(max_length=10)
	private = models.BooleanField(default=False)
	data_connection = models.ForeignKey(DataConnection)
	data_type = models.IntegerField(choices=DATATYPECHOICE, default=0) 
	old_data_choice = models.IntegerField(choices=OLDDATACHOICE, default=0) 
	csv_seprator = models.CharField(max_length=5,null=True,blank=True)
	new_row_on_number = models.BooleanField(default=False)
	new_row_on_number_name = models.CharField(max_length=30,null=True,blank=True)
	overwrite_fields = models.CharField(max_length=50,null=True,blank=True)
	data_from_date = models.DateTimeField(null=True)
	data_to_date = models.DateTimeField(null=True)
	date_last_update = models.DateTimeField(default=None, null=True)
	update_interval = models.CharField(
        max_length=20,
        choices=(
            ('day', 'Day'),
            ('week', 'Week'),
            ('month', 'Month'),
            ('year', 'Year'),
        ),
        default="month")
	quality_of_source = models.FloatField(default=5.0)#to be determened
	flags = models.ManyToManyField(DataSourceFlags)

	def __unicode__(self):
		return self.name

	# def process(self):
	# 	if self.data_type == 1:
	# 		parser = xmlParse.xmlImport()
	# 	elif self.data_type == 0:
	# 		parser = csvParse.CsvImport()
	# 	connection = self.data_connection
	# 	parser.connect(connection.name,connection.username,connection.password,connection.host,connection.port,self.prefix)
	# 	#get the file 



class DataSourceComment(models.Model):

	data_source = models.ForeignKey(DataSource)
	comment = models.TextField()
	user = models.ForeignKey(User)



class DataModelClass(models.Model):
	data_source = models.ForeignKey(DataSource)
	name = models.CharField(max_length=30)
	default_cluster_id = models.CharField(max_length=5)
	translated_name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.name

class DataModelGroup(models.Model):
	data_model_class = models.ForeignKey(DataModelClass)
	name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.name

class DataModelSubGroup(models.Model):
	data_model_group = models.ForeignKey(DataModelGroup)
	name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.name



class DataModelProperty(models.Model):
	data_model_class = models.ForeignKey(DataModelClass)
	name = models.CharField(max_length=30)
	data_model_subgroup = models.ForeignKey(DataModelSubGroup)
	translated_name = models.CharField(max_length=30)
	property_type = models.CharField(max_length=30)
	property_values = models.TextField() # possible values is more than 20 
	def __unicode__(self):
		return "%s.%s" % (self.data_model_class.name, self.name)

class DataModelEdge(models.Model):
	data_source = models.ForeignKey(DataSource)
	class_in = models.ForeignKey(DataModelClass,related_name='class_in')
	class_out = models.ForeignKey(DataModelClass,related_name='class_out')

class DataModelEdgeProperty(models.Model):
	data_model_edge = models.ForeignKey(DataModelEdge)
	name = models.CharField(max_length=30)
	property_type = models.CharField(max_length=30)

	def __unicode__(self):
		return "%s.%s" % (self.data_model_edge.name, self.name)

class DataModelQuery(OrderedModel):

    class Meta(OrderedModel.Meta):
        verbose_name = "DataModel Query"
        verbose_name_plural = "DataModel Queries"
    data_source = models.ForeignKey(DataSource)
    name = models.CharField(max_length=30)
    query = models.TextField()
    run_after_update = models.BooleanField(default=False)

    def __str__(self):
        pass
    def __unicode__(self):
		return self.name

#pivot point extremely importand
class DataModelPivotPoint(models.Model):
	name = models.CharField(max_length=30)
	pivot_type = models.CharField(max_length=30)
	create_script = models.TextField(null=True,blank=True)



class DataProject(models.Model):

	user = models.ForeignKey(User)
	name = models.CharField(max_length=56)
	description = models.TextField(null=True,blank=True)


    
	

	def __unicode__(self):
   		return self.name

class DataSet(models.Model):
	data_project = models.ForeignKey(DataProject)
	name = models.CharField(max_length=56)
	description = models.TextField(null=True,blank=True)

	def __unicode__(self):
   		return self.name

class DataSetStream(models.Model):

	data_set = models.ForeignKey(DataSet)
	data_stream = models.ForeignKey(DataSource)
   	class Meta:
   		verbose_name = "Data set stream"
   		verbose_name_plural = "Data set streams"

	def __unicode__(self):
		return self.data_set.name+'-'+self.data_stream.name

class DataSetStreamProperty(models.Model):

	ACTIONCHOICE = (
	    (0, 'SUM'),
	    (1, 'AVG'),
	    (2, 'MAX'),
	    (3,	'MIN'),
	    (4,	'GROUP BY'),

	)
	data_set_stream = models.ForeignKey(DataSetStream)
	data_model_property = models.ForeignKey(DataModelProperty)
	action = models.IntegerField(choices=ACTIONCHOICE, default=0) 
	filter_value = models.CharField(max_length=512,null=True,blank=True)

	def __unicode__(self):
		return self.data_model_property.translated_name


     
    

    


    















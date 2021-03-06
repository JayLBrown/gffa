from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from . forms import PlanetForm
from . models import Film, Person, Planet, Species, Starship, Vehicle, FilmPlanet


class HomePageView(generic.TemplateView):
	template_name = 'webapp/home.html'


class AboutPageView(generic.TemplateView):
	template_name = 'webapp/about.html'


# def about(request):
#     # stripe_key = settings.STRIPE_KEYS['publishable']
#     # data = cache.get('resource_data')
#     # if not data:
#     #     data = get_resource_stats()
#     #     cache.set('resource_data', data, 10000)
#     # data['stripe_key'] = stripe_key

#     data = 'A long time ago in a galaxy far, far away.'
#     return render(request, "about.html", data)


class DocsPageView(generic.TemplateView):
	template_name = 'webapp/docs.html'


class RootPageView(generic.TemplateView):
	template_name = 'webapp/root.html'

class FilmPageView(generic.TemplateView):
	template_name = 'webapp/film_docs.html'


class PersonPageView(generic.TemplateView):
	template_name = 'webapp/person_docs.html'


class PlanetPageView(generic.TemplateView):
	template_name = 'webapp/planet_docs.html'


class SpeciesPageView(generic.TemplateView):
	template_name = 'webapp/species_docs.html'


class StarshipPageView(generic.TemplateView):
	template_name = 'webapp/starship_docs.html'


class VehiclePageView(generic.TemplateView):
	template_name = 'webapp/vehicle_docs.html'


class FilmDetailView(generic.DetailView):
	model = Film
	context_object_name = 'films'
	template_name = 'webapp/film_detail.html'

	def get_object(self):
		return super().get_object()

class FilmListView(generic.ListView):
	model = Film
	context_object_name = 'films'
	template_name = 'webapp/films.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Film.objects.all()
		# return Person.objects.select_related('homeworld').order_by('name')


class PersonDetailView(generic.DetailView):
	model = Person
	context_object_name = 'persons'
	template_name = 'webapp/person_detail.html'

	def get_object(self):
		person = super().get_object()
		return person


class PersonListView(generic.ListView):
	model = Person
	context_object_name = 'persons'
	template_name = 'webapp/persons.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Person.objects.all()
		# return Person.objects.select_related('homeworld').order_by('name')




class PlanetDetailView(generic.DetailView):
	model = Planet
	context_object_name = 'planets'
	template_name = 'webapp/planet_detail.html'

	def get_object(self):
		planet = super().get_object()
		return planet

class PlanetListView(generic.ListView):
	model = Planet
	context_object_name = 'planets'
	template_name = 'webapp/planets.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Planet.objects.all()
		# return Person.objects.select_related('homeworld').order_by('name')


@method_decorator(login_required, name='dispatch')
class PlanetCreateView(generic.View):
	model = Planet
	form_class = PlanetForm
	success_message = "Planet created successfully!"
	template_name = 'webapp/planet_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = PlanetForm(request.POST)
		if form.is_valid():
			planet = form.save(commit=False)
			planet.save()

		for planet in form.cleaned_data['planets']:
			Planet.objects.create(planet=planet)

		return render(request, 'webapp/planet_new.html', {'form': form})

	def get(self, request):
		form = PlanetForm()
		return render(request, 'webapp/planet_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PlanetUpdateView(generic.UpdateView):
	model = Planet
	form_class = PlanetForm
	context_object_name = 'planet'
	success_message = "Planet updated successfully!"
	template_name = 'webapp/planet_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		planet = form.save(commit=False)
		planet.save()

		return HttpResponseRedirect(planet.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class PlanetDeleteView(generic.DeleteView):
	model = Planet
	success_message = "Planet deleted successfully!"
	success_url = reverse_lazy('planet')
	context_object_name = 'planet'
	template_name = 'webapp/planet_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete Planet entries
		Planet.objects \
			.filter(planet_id=self.object.planet_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

class SpeciesDetailView(generic.DetailView):
	model = Species
	context_object_name = 'species'
	template_name = 'webapp/species_detail.html'

	def get_object(self):
		species = super().get_object()
		return species


class SpeciesListView(generic.ListView):
	model = Species
	context_object_name = 'species'
	template_name = 'webapp/species.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Species.objects.all()
		# return Species.objects.select_related('homeworld').order_by('name')


class StarshipDetailView(generic.DetailView):
	model = Starship
	context_object_name = 'starships'
	template_name = 'webapp/starship_detail.html'

	def get_object(self):
		starship = super().get_object()
		return starship


class StarshipListView(generic.ListView):
	model = Starship
	context_object_name = 'starships'
	template_name = 'webapp/starships.html'


	def get_queryset(self):
		return Starship.objects.all()
		# return Starship.objects.select_related('?').order_by('?')


class VehicleDetailView(generic.DetailView):
	model = Vehicle
	context_object_name = 'vehicles'
	template_name = 'webapp/vehicle_detail.html'

	def get_object(self):
		return super().get_object()


class VehicleListView(generic.ListView):
	model = Vehicle
	context_object_name = 'vehicles'
	template_name = 'webapp/vehicles.html'

	def get_queryset(self):
		return Vehicle.objects.all()

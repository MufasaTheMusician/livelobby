from django.views.generic.edit import FormMixin
from django.shortcuts import reverse
from events.forms import JoinForm
from events.models import Event
from django.views.generic import DetailView, ListView


class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event


class EventView(DetailView, FormMixin):
    template_name = 'events/event.html'
    model = Event
    form_class = JoinForm

    def get_success_url(self):
        return reverse('event_view', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['form'] = JoinForm(initial={'event': self.object})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(EventView, self).form_valid(form)
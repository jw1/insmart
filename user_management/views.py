from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from insmart_core.search import get_query
from user_management.models import UserProfile

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_active']


def user_list(request, template_name='user_management/user_list.html'):

    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, UserForm.Meta.fields) # I search on all fields.  Adjust as needed.
        users = User.objects.filter(entry_query).order_by('username')
    else:
        users = User.objects.all().order_by('username')

    data = {}
    data['object_list'] = users
    return render(request, template_name, data)

def user_create(request, template_name='user_management/user_form.html'):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, template_name, {'form':form})

def user_update(request, pk, template_name='user_management/user_form.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, template_name, {'form':form})

def user_delete(request, pk, template_name='user_management/user_confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('user_list')
    return render(request, template_name, {'object':user})

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def handle_new_job(sender, **kwargs):
    user = kwargs.get('instance')
    if hasattr(user,'userprofile') == False:
        UserProfile.objects.get_or_create(user=user)

#
# This section here renders the list as a PDF, to fulfill the reporting
# requirement.  We said we'd investigate and maybe generate one in our FRs.
#
# This is very quick and dirty.
#
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def user_list_as_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    width, height = letter

    y = height
    p.drawString(x=300, y=y, text="InSmart Users")

    y-=25
    p.drawString(x=25, y=y, text="ID #")
    p.drawString(x=75, y=y, text="First Name")
    p.drawString(x=175, y=y, text="Last Name")
    p.drawString(x=275, y=y, text="Email")
    p.drawString(x=450, y=y, text="Super")
    p.drawString(x=500, y=y, text="Active")

    y -= 25
    for user in User.objects.all():
        p.drawString(x=25, y=y, text=str(user.id))
        p.drawString(x=75, y=y, text=user.first_name)
        p.drawString(x=175, y=y, text=user.last_name)
        p.drawString(x=275, y=y, text=user.email)
        p.drawString(x=450, y=y, text=str(user.is_superuser))
        p.drawString(x=500, y=y, text=str(user.is_active))
        y-= 25

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
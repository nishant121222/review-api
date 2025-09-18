# businesses/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Business
from accounts.models import AdminUser

@method_decorator(csrf_exempt, name='dispatch')
class BusinessListView(View):
    """
    Admin: List all businesses (for owner/admin)
    GET /api/admin/businesses/
    """
    def get(self, request):
        # Only allow authenticated admin users
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        # Owners see all their businesses; admins see their assigned business
        if request.user.role == 'owner':
            businesses = Business.objects.filter(owner=request.user)
        else:
            businesses = Business.objects.filter(owner=request.user)

        data = [
            {
                'id': b.id,
                'name': b.name,
                'google_location_id': b.google_location_id,
                'account_id': b.account_id,
                'created_at': b.created_at.isoformat(),
                'settings': b.settings
            }
            for b in businesses
        ]
        return JsonResponse({'businesses': data})


@method_decorator(csrf_exempt, name='dispatch')
class BusinessDetailView(View):
    """
    Admin: Get or update a specific business
    GET /api/admin/businesses/<id>/
    PUT /api/admin/businesses/<id>/
    """
    def get(self, request, business_id):
        try:
            business = Business.objects.get(id=business_id)
            if request.user != business.owner and request.user.role != 'owner':
                return JsonResponse({'error': 'Permission denied'}, status=403)

            return JsonResponse({
                'id': business.id,
                'name': business.name,
                'google_location_id': business.google_location_id,
                'account_id': business.account_id,
                'settings': business.settings,
                'created_at': business.created_at.isoformat()
            })
        except Business.DoesNotExist:
            return JsonResponse({'error': 'Business not found'}, status=404)

    def put(self, request, business_id):
        try:
            business = Business.objects.get(id=business_id)
            if request.user != business.owner:
                return JsonResponse({'error': 'Permission denied'}, status=403)

            data = json.loads(request.body)

            business.name = data.get('name', business.name)
            business.google_location_id = data.get('google_location_id', business.google_location_id)
            business.account_id = data.get('account_id', business.account_id)
            business.settings = data.get('settings', business.settings)

            # Handle google_api_creds securely
            if 'google_api_creds' in data:
                business.google_api_creds = data['google_api_creds']

            try:
                business.full_clean()  # Runs model validation
                business.save()
                return JsonResponse({'success': True, 'id': business.id})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        except Business.DoesNotExist:
            return JsonResponse({'error': 'Business not found'}, status=404)


# Assign views
business_list = BusinessListView.as_view()
business_detail = BusinessDetailView.as_view()
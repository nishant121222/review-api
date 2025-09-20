from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.contrib.auth import get_user_model
from .models import Business

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class BusinessListView(View):
    """
    Admin: List all businesses (for owner/admin)
    GET /api/admin/businesses/
    """
    def get(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return JsonResponse({'status': False, 'message': 'Authentication required', 'data': []}, status=401)

        # Owners see all their businesses
        businesses = Business.objects.filter(owner=request.user)

        if not businesses.exists():
            return JsonResponse({'status': False, 'message': 'No Records Found', 'data': []})

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
        return JsonResponse({'status': True, 'message': 'Businesses fetched successfully', 'data': data})


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
            if request.user != business.owner:
                return JsonResponse({'status': False, 'message': 'Permission denied', 'data': None}, status=403)

            return JsonResponse({
                'status': True,
                'message': 'Business fetched successfully',
                'data': {
                    'id': business.id,
                    'name': business.name,
                    'google_location_id': business.google_location_id,
                    'account_id': business.account_id,
                    'settings': business.settings,
                    'created_at': business.created_at.isoformat()
                }
            })
        except Business.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Business not found', 'data': None}, status=404)

    def put(self, request, business_id):
        try:
            business = Business.objects.get(id=business_id)
            if request.user != business.owner:
                return JsonResponse({'status': False, 'message': 'Permission denied', 'data': None}, status=403)

            data = json.loads(request.body)

            business.name = data.get('name', business.name)
            business.google_location_id = data.get('google_location_id', business.google_location_id)
            business.account_id = data.get('account_id', business.account_id)
            business.settings = data.get('settings', business.settings)
            if 'google_api_creds' in data:
                business.google_api_creds = data['google_api_creds']

            try:
                business.full_clean()
                business.save()
                return JsonResponse({'status': True, 'message': 'Business updated successfully', 'data': {'id': business.id}})
            except Exception as e:
                return JsonResponse({'status': False, 'message': str(e), 'data': None}, status=400)

        except Business.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Business not found', 'data': None}, status=404)


# Assign views
business_list = BusinessListView.as_view()
business_detail = BusinessDetailView.as_view()

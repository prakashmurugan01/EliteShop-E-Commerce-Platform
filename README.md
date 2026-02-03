# EliteShop E-Commerce Platform

A full-featured Django-based e-commerce application with product management, shopping cart, order processing, user authentication, and admin panel.

## Features

### Core Functionality
- **Product Management**: Browse, filter by category, view detailed product pages
- **Shopping Cart**: Add/remove items, update quantities, persistent cart management
- **Order Management**: Place orders, view order history, order confirmation emails
- **User Accounts**: Registration, login, profile management, saved addresses
- **Admin Panel**: Dashboard, product/category/order management, order status tracking
- **Delivery Tracking**: Track order delivery status with real-time updates

### Technical Stack
- **Backend**: Django 4.2.16, Python 3.13
- **Database**: SQLite3 (configurable to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, Vanilla JavaScript, Crispy Forms
- **File Storage**: Local filesystem (ImageField for products)
- **Authentication**: Django built-in auth system

### Applications
1. **products** - Product catalog, categories, filtering
2. **cart** - Shopping cart management
3. **orders** - Order creation, management, status tracking
4. **accounts** - User registration, login, profiles, addresses
5. **delivery** - Delivery tracking and status updates
6. **adminpanel** - Admin interface for managing products/categories/orders

## Installation

### Prerequisites
- Python 3.13+
- pip, virtualenv

### Setup Steps

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR-USERNAME/ecommerce_core.git
cd ecommerce_core
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**:
```bash
python manage.py createsuperuser
```

6. **Start development server**:
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`

## Project Structure

```
ecommerce_core/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database
├── ecommerce_core/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # User management app
│   ├── models.py           # UserProfile, Address models
│   ├── views.py
│   ├── forms.py
│   └── admin.py
├── products/               # Product catalog app
│   ├── models.py           # Product, Category models
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── management/commands/fix_slugs.py
├── cart/                   # Shopping cart app
│   ├── models.py           # CartItem model
│   ├── views.py
│   └── admin.py
├── orders/                 # Order management app
│   ├── models.py           # Order, OrderItem, Coupon models
│   ├── views.py
│   ├── forms.py
│   └── admin.py
├── delivery/               # Delivery tracking app
│   ├── models.py           # DeliveryTracking, DeliveryStatusUpdate
│   ├── views.py
│   └── admin.py
├── adminpanel/             # Admin dashboard app
│   ├── views.py
│   └── urls.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   ├── products/
│   ├── cart/
│   ├── orders/
│   ├── accounts/
│   └── adminpanel/
├── static/                 # CSS, JavaScript
│   ├── css/style.css
│   └── js/script.js
└── media/                  # User-uploaded product images
```

## Key Models

### Product
- name, slug, description, price, discount_price, stock
- category (ForeignKey to Category)
- image, is_trending, created_at, updated_at

### Category
- name, slug, description, icon

### Order
- user (ForeignKey to User)
- status (PLACED, CONFIRMED, PACKED, SHIPPED, OUT_FOR_DELIVERY, DELIVERED, CANCELLED)
- total_price, created_at, updated_at

### CartItem
- user, product, quantity

### Address
- user, street, city, state, zipcode, country

## API Endpoints

### Products
- `GET /products/` - List all products
- `GET /products/?category=<id>` - Filter by category
- `GET /product/<slug>/` - Product detail page

### Cart
- `POST /cart/add/` - Add to cart
- `POST /cart/update/` - Update quantity
- `GET /cart/` - View cart
- `GET /cart/count/` - Get cart item count

### Orders
- `GET /orders/my-orders/` - User's orders
- `GET /orders/order-detail/<id>/` - Order details
- `POST /orders/place-order/` - Create order
- `GET /orders/order-confirmation/<id>/` - Order confirmation

### Accounts
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /accounts/profile/` - User profile
- `POST /accounts/add-address/` - Add address
- `GET /accounts/logout/` - Logout

### Admin Panel
- `GET /admin-panel/dashboard/` - Admin dashboard
- `GET /admin-panel/products/` - Manage products
- `GET /admin-panel/products/add/` - Add product
- `GET /admin-panel/products/edit/<id>/` - Edit product
- `GET /admin-panel/categories/` - Manage categories
- `GET /admin-panel/orders/` - Manage orders
- `GET /admin-panel/orders/update/<id>/` - Update order status

## Configuration

### Settings (`ecommerce_core/settings.py`)
- `DEBUG = True` (set to False in production)
- `ALLOWED_HOSTS = ['*']` (configure for production)
- `DATABASES` - SQLite by default
- `INSTALLED_APPS` - All custom apps registered
- `TEMPLATES['DIRS']` - Points to `/templates`
- `CRISPY_TEMPLATE_PACK = 'bootstrap5'`

### Static & Media Files
- Static files: `/static/`
- Media files: `/media/`
- Configure `STATIC_URL` and `MEDIA_URL` in settings

## Management Commands

### Fix Product Slugs
Normalize all product slugs to URL-safe values:
```bash
python manage.py fix_slugs
```

## Testing

Run the development server:
```bash
python manage.py runserver
```

Access:
- Frontend: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin-panel/dashboard/
- Django Admin: http://127.0.0.1:8000/admin/

## Deployment

### Production Checklist
1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use environment variables for `SECRET_KEY`
4. Switch to PostgreSQL or MySQL
5. Use WhiteNoise for static files
6. Configure email backend for order notifications
7. Use a production WSGI server (Gunicorn, uWSGI)
8. Set up HTTPS with SSL certificate
9. Configure CORS if using separate frontend

### Deploy to Heroku
```bash
heroku create your-app-name
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Dependencies

- Django==4.2.16
- Pillow==11.0.0
- django-crispy-forms==2.3
- crispy-bootstrap5==2024.10

See `requirements.txt` for full list.

## Known Issues & Future Enhancements

### Known Issues
- Cart updates require page reload for some operations
- Product slug normalization handles special characters but may truncate long names

### Future Features
- Payment gateway integration (Stripe, PayPal)
- Email notifications for orders
- Product reviews and ratings
- Wishlist functionality
- Advanced search and filtering
- Inventory management alerts
- API with Django REST Framework
- Mobile app
- Multi-currency support
- Coupon management system

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, bugs, or feature requests, please open a GitHub issue or contact support.

## Project Status

✅ **Completed**
- Core e-commerce functionality
- Admin panel for management
- User authentication
- Product catalog with filtering
- Shopping cart
- Order processing
- Admin dashboard

🔄 **In Progress**
- Cart UI improvements
- Category management improvements

📋 **To Do**
- Payment integration
- Email notifications
- Advanced analytics
- Performance optimization

---

**Last Updated**: November 28, 2025
**Version**: 1.0.0
#   e c o m m e r c e _ c o r e  
 #   e c o m m e r c e _ c o r e 1  
 #   e c o m m e r c e _ c o r e  
 #   e c o m m e r c e _ c o r e  
 #   e c o m m e r c e _ c o r e  
 #   E l i t e S h o p - E - C o m m e r c e - P l a t f o r m  
 #   E l i t e S h o p - E - C o m m e r c e - P l a t f o r m  
 
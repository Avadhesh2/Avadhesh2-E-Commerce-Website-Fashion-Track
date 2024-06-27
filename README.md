
# E-Commerce Website - Fashion Track

Fashion Track is a robust e-commerce web application designed to provide a seamless shopping experience. It offers a variety of functionalities including admin product management, user authentication, profile management, shopping cart functionality, and payment integration with Razorpay.

## Features

- **Admin Panel**: Admin can add, edit, and delete products on the website.
- **User Authentication**: Users can sign up, log in, and reset passwords through email links.
- **Profile Management**: Users can view and update their profile information.
- **Shopping Cart**: Users can add products to their cart, view items in the cart, and proceed to checkout.
- **Razorpay Payment Integration**: Secure payment processing through Razorpay.
- **Order History**: Users can view their past orders and their statuses.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Avadhesh2/E-Commerce-Website-Fashion-Track-.git
   cd E-Commerce-Website-Fashion-Track-
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

6. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`.

## Usage

### Admin Panel

- Log in with the superuser account created during the installation.
- Navigate to the admin panel at `http://127.0.0.1:8000/admin`.
- Add, edit, or delete products from the product management section.

### User Authentication

- Users can sign up for a new account or log in to an existing account.
- Password reset links are sent to the user's email for secure password recovery.

### Profile Management

- Users can view and update their profile information from the profile page.
- Order history and current cart items are also accessible from the profile page.

### Shopping Cart

- Add products to the cart from the product listing or product detail page.
- View the cart and proceed to checkout to complete the purchase.

### Payment Integration

- Payments are processed securely using Razorpay.
- Users receive email notifications for successful payments and order updates.

## Contributing

We welcome contributions to enhance the functionality of Fashion Track. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or issues, please open an issue on GitHub.

---

Thank you for using Fashion Track! Happy shopping!
```

To add this README file to your GitHub repository:

1. Save the above content in a file named `README.md`.
2. Add the README file to your project directory.
3. Commit the README file and push it to GitHub:
   ```sh
   git add README.md
   git commit -m "Add README file"
   git push origin master
   ```

This will add the README file to your GitHub repository and display it on the repository's main page.

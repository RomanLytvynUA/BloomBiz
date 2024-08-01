
<h3 align="center">
  <img src="https://github.com/user-attachments/assets/34edd6de-68f4-481b-bfa6-f97441c9857b" alt="Logo" width="150" height="150">
  <br>
  BloomBiz
</h3>
<p align="center">A comprehensive flower shop management tool that covers inventory, orders, customer management, and financial analytics.
<br/>
<br/>
<a href="https://github.com/RomanLytvynUA/BloomBiz/issues/new?assignees=RomanLytvynUA&labels=bug&projects=&template=raise-a-defect.md">Report Bug</a>
<a href="https://github.com/RomanLytvynUA/BloomBiz/issues/new?assignees=RomanLytvynUA&labels=enhancement&projects=&template=feature_request.md">Request Feature</a>
</p>
</div>

 ## About

BloomBiz is an all-in-one flower shop management tool designed to streamline and enhance the operations of flower shops. It provides functionalities for inventory management, order processing, customer relationship management, sales analytics, etc.

Key features:

- **Customer Relationship Management:** A simple solution for storing customer data that integrates easily with other app tools.
- **Inventory Management:** Control product decommissioning, in-stock quantities, and pricing in one centralized location.
- **Expense Registry:** A feature to view, add, and modify expenses and supplies, integrated with inventory management to update stock quantities and prices accordingly.
- **Order Registry:** A system to view, add, and modify orders, integrated with customer data and inventory management, enabling price recommendations.
- **Statistics:** Provides clear and useful insights into the shop's cash flow, profit, and other financial metrics that impact business performance.
- **Multi-language support:** New localization can be added easily, currently supports Ukrainian and English languages.

 ## Built With

**Front end:**
  - [Vue](https://vuejs.org)
  - [Vue-i18n](https://vue-i18n.intlify.dev/)
  - [Bootstrap](https://getbootstrap.com)
  - [Chart.js](https://www.chartjs.org)
  - [date-fns](https://date-fns.org)
  - [JQuery](https://jquery.com)

**Back end:**
  - [Flask](https://flask.palletsprojects.com)
  - [Flask-JWT](https://flask-jwt-extended.readthedocs.io)
  - [SQLAlchemy](https://www.sqlalchemy.org)
  - [Pytest](https://pytest.org)
  
 ## Getting Started
 ### Locally
 #### Pre-requisites:
   - Python
   - Node.js
   - Postgress *(with a dedicated db)*
 #### Installation:
  1. Set environment variables.
      - Set "BB_DB_URI" as to your db URI.
      - Set "JWT_SECRET_KEY".
  2. Install back-end requirements.
       - ```cd "Back end"```
       - ```pip install -r requirements.txt```
  3. Set up the db. *(first run only)*
       - ```python db_setup.py```
  4. Run the back end.
       - ```python run.py```
  5. Install front-end requirements.
       - ```cd "Front end"```
       - ```npm install```
  6. Run the front end.
       - ```npm run build```
  7. Populate demonstration data, add user, add registration code, etc. *(optional)*
       - ```cd "Back end"```
       - ```python dashboard.py```
       - Select an operation and follow instructions. 
 ### Via Docker
 #### Pre-requisites:
   - Docker engine
 #### Installation:
  1. Change environment configuration. *(optional)*
      - Change db credentials.
      - Change the BB_DB_URI variable of the back end accordingly to changed db credentials.
      - Change the JWT_SECRET_KEY variable of the back end.
  2. Run docker compose.
       - ```docker-compose up```
  4. Run the back-end shell.
       - ```docker-compose exec backend /bin/bash```
  5. Set up the db. *(first run only)*
       - ```python db_setup.py```
  6. Populate demonstration data. *(optional)*
       - ```python fake_data.py```
  7. Add a user. *(optional)*
     - Run the dashboard.
         - ```python dashboard.py```
     - Select "Create an account" and follow instructions.
## Roadmap
- [x] Suppliers management
- [x] CRM
- [x] Expenses management
- [x] Orders management
- [x] Stock management
- [x] Multi-language Support
- [x] Settings
- [x] Assortment management
- [x] Profit statistic
- [x] Auth
- [ ] "Summarize to print" feature
- [ ] Decomission statistic
- [ ] Customer statistic
- [ ] Customer summary
- [ ] Calendar
- [ ] Multi-store support

## Documentation

### Dashboard script
**Description:**<br>
A simple dashboard with some features to manage the app. Current features: generate a registration code, view registration codes, invalidate all registration codes, invalidate a registration code, view users, delete an account, create an account, and populate fake data.
<br>**How to run:**<br>
```python dashboard.py```

### Fake data script
**Description:**<br>
The script generates random demonstration data (orders, expenses, suppliers, customers, etc.). By default, the starting date is the first of January (the beginning of the current year), and the offset can be adjusted with flags --years, --months, --days.
The default language is English, but it can be changed to Ukrainian with the "-lang ukr" flag.
<br>**How to run:**<br>
```python fake_data.py --years YEARS_OFFSET --months MONTHS_OFFSET --days DAYS_OFFSET --lang eng\ukr```

### Database setup script
**Description:**<br>
The script creates all necessary db tables. By default the language is English, but it can be changed to Ukrainian with the "-lang ukr" flag.
<br>**How to run:**<br>
```python db_setup.py --lang eng\ukr```





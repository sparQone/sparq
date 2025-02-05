# sparQ

sparQ is a modular HR/Team Management and general business application platform built with Python and Flask. It provides a flexible, plugin-based 
architecture for managing core business operations, allowing businesses to enable or disable modules based on their needs.  

![sparQ Dashboard](modules/core/views/assets/images/screen1.png)  

  

## Features

- **Modular System**: Easily extend functionality with independent modules.
- **Dynamic Module Loading**: Modules are auto-discovered and loaded.
- **Extensible Plugin Architecture**: Uses `pluggy` for module integration.
- **Language Support**: Supports multiple languages and user-specific settings.
- **Built-in Core Modules**:
  - **Core**: Authentication, module management, and UI framework.
  - **People**: Employee management, roles, and departments.
- **Additional Modules**:
  - **Books**: Accounting and bookkeeping.
  - **E-Sign**: Digital document signing.
  - **Tasks**: Task and appointment management.
  - **Weather & Clock**: Utility modules (For demonstration purpose)
- **Modern UI**: HTMX for dynamic updates, Bootstrap styling, and responsive layouts.

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- SQLAlchemy
- HTMX

### Installation


Requirements:
- Python 3.10+
- pip
- git
- OSX/Linux


Get the code:
```bash
git clone https://github.com/remarqable/sparq
cd sparq
```

Install venv if you don't have it:
```bash
sudo apt install python3-venv
```

Create a virtual environment and install the dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the app:
```bash
python3 app.py
```

Access the application at `http://localhost:8000`.

## Module System

sparQ follows a "building block" approach where functionality is divided into independent modules.

[How to write a new module - (Applications and Extensions)](https://github.com/sparqone/sparq/blob/master/docs/Write%20a%20module%20-%20App.md)


## Security
- User authentication and role-based access control.
- Admin privileges for module management.
- Secure session management.

## Roadmap
- Additional business modules
- Enhanced API integration
- Mobile app support
- Customization options
- 

## License
sparQ is released under the Apache-2.0 license

## Contributing
We welcome contributions! Please submit issues or pull requests on [GitHub](https://github.com/remarqable/sparq).

## Contact
For questions or support, reach out to [asim95@gmail.com](mailto:asim95@gmail.com).


# Main package is arched in order to run tests on all arches
%global debug_package %{nil}

Name:           python-f2py-cmake
Version:        0.0.0
Release:        %autorelease
Summary:        F2Py helpers for CMake

License:        Apache-2.0
URL:            https://github.com/scikit-build/f2py-cmake
Source:         %{pypi_source f2py_cmake}

BuildRequires:  python3-devel
BuildRequires:  python3-numpy-f2py
# Testing dependences
BuildRequires:  cmake
BuildRequires:  gfortran

%global _description %{expand:
This provides helpers for using F2Py. Use:

include(UseF2Py)
}

%description %_description

%package -n python3-f2py-cmake
Summary:        %{summary}
Requires:       cmake
Requires:       python3-numpy-f2py
BuildArch:      noarch
%description -n python3-f2py-cmake %_description


%prep
%autosetup -n f2py_cmake-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l f2py_cmake


%check
%pyproject_check_import
%pytest


%files -n python3-f2py-cmake -f %{pyproject_files}
%{_bindir}/f2py-cmake
%doc README.md


%changelog
%autochangelog

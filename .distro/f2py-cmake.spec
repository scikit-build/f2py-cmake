Name:           f2py-cmake
Version:        0.0.0
Release:        %autorelease
Summary:        F2Py helpers for CMake

License:        Apache-2.0
URL:            https://github.com/scikit-build/f2py-cmake
Source:         %{pypi_source f2py_cmake}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-numpy-f2py
# Testing dependences
BuildRequires:  cmake
BuildRequires:  gfortran
Requires:       cmake
Requires:       python3-devel
Requires:       python3-numpy-f2py

%global _description %{expand:
This provides helpers for using F2Py. Use:

include(UseF2Py)
}

%description %_description

CMake module files.

%package -n python3-f2py-cmake
Summary:        %{summary}
Requires:       f2py-cmake = %{version}-%{release}
%description -n python3-f2py-cmake %_description

Python package.


%prep
%autosetup -n f2py_cmake-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l f2py_cmake
# Move the actual CMake modules to /usr/share/cmake
mkdir -p %{buildroot}%{_datadir}/cmake/Modules
mv %{buildroot}%{python3_sitelib}/f2py_cmake/cmake/*.cmake %{buildroot}%{_datadir}/cmake/Modules/
ln -rs %{buildroot}%{_datadir}/cmake/Modules/*.cmake %{buildroot}%{python3_sitelib}/f2py_cmake/cmake/


%check
%pyproject_check_import
%pytest


%files
%{_datadir}/cmake/Modules/*.cmake
%license LICENSE
%doc README.md

%files -n python3-f2py-cmake -f %{pyproject_files}
%{_bindir}/f2py-cmake


%changelog
%autochangelog

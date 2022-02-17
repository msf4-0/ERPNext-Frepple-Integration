# ERPNext-Frepple Integration
<a href="https://github.com/msf4-0/ERPNext-Frepple-Integration/blob/master/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/msf4-0/ERPNext-Frepple-Integration.svg?color=blue">
</a>
<a href="https://github.com/msf4-0/ERPNext-Frepple-Integration/releases">
    <img alt="Releases" src="https://img.shields.io/github/release/msf4-0/ERPNext-Frepple-Integration?color=success" />
</a>
<a href="https://github.com/msf4-0/ERPNext-Frepple-Integration/releases">
    <img alt="Downloads" src="https://img.shields.io/github/downloads/msf4-0/ERPNext-Frepple-Integration/total.svg?color=success" />
</a>
<a href="https://github.com/msf4-0/ERPNext-Frepple-Integration/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/msf4-0/ERPNext-Frepple-Integration?color=blue" />
</a>
<a href="https://github.com/msf4-0/ERPNext-Frepple-Integration/pulls">
    <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/msf4-0/ERPNext-Frepple-Integration?color=blue" />
</a>


## [Frepple](https://github.com/frePPLe/frepple) integration for [Frappe web framework](https://github.com/frappe/frappe)
Frepple Custom App built based on Frepple Advance Planning and Scheduling software. It was built to integrate with ERPNext.

## Prerequisite
1. Installed the Frepple and successfully launched it on the localhost. 
2. Installed the ERPNext and successfully launched it on the localhost.

## The App Contains
1. Export data from ERPNext to Frepple by a few button click.
2. Generate the plan in Frepple custom app itself, with the flexibility to change the plan constraint.
3. Import the manufacturing order and purchase order from Frepple to ERPNext.
4. Embed Frepple page into ERPNext using iframe. User is able to create the iframe page via `Frepple Custom Page`.
5. Generate the work order and purchase order in ERPNext based on the result from Frepple.
6. Sync the status of work order and purchase order between ERPNext and Frepple.

## Usage
### 1. Installation
Navigate to the bench directory and run the following command:
> bench get-app frepple https://github.com/Drayang/ERPNext-Frepple.git

Install the app onto your site.
> bench --site [your.site.name] install-app frepple 

Bench start
> bench start



#### License
MIT
=======


## Contributors
1. [Drayang Chua Kai Yang](https://github.com/Drayang)
2. [Lee Xin Yue](https://github.com/leexy0)
3. [Chia Jun Shen](https://github.com/chiajunshen)

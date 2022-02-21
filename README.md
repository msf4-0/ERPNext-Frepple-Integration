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
Frepple Custom App built based on Frepple Advanced Planning and Scheduling software. It was built to integrate with ERPNext, act as a connector that allow bidirectional data transfer between Frepple and ERPNext. It also used to map the data type between frepple and ERPNext since both software do not use the same data structure and format.


## Prerequisite
1. Installed the Frepple and successfully launched it on the localhost.
2. Installed the ERPNext and successfully launched it on the localhost.

## The App Contains
1. Export data from ERPNext to Frepple with a few clicks.
<img width="857" alt="WeChat Screenshot_20220217113754" src="https://user-images.githubusercontent.com/53387856/154400564-0aa408c7-cae6-431e-be03-fe6451e6b87a.png">

2. Generate the plan in Frepple custom app itself, with configurable constraints.
<img width="865" alt="Frepple run plan page" src="https://user-images.githubusercontent.com/53387856/154400669-c4beafb0-181b-440f-a73e-4c8e69e2ce04.png">

3. Import the manufacturing orders and purchase orders from Frepple to ERPNext.

4. Embed Frepple page into ERPNext user interface using iframe. Access the frepple screens through `Frepple Custom Page`.
<img width="854" alt="Frepple custom page" src="https://user-images.githubusercontent.com/53387856/154400895-02414e51-bdbf-4c38-9861-98dbfd6eb425.png">

5. Generate the work order and purchase order in ERPNext based on the result from Frepple.
<img width="872" alt="Frepple manufacturing order " src="https://user-images.githubusercontent.com/53387856/154401045-4a6ad63b-5583-41ee-b092-f5de0295698c.png">

6. Sync the status of work orders and purchase orders between ERPNext and Frepple.

## Usage
### 1. Installation
Navigate to the bench directory and run the following command:
> bench get-app frepple https://github.com/msf4-0/ERPNext-Frepple-Integration.git

Install the app onto your site.
> bench --site [your.site.name] install-app frepple

Bench start
> bench start

The Frepple custom app main page.
<img width="866" alt="Frepple module main page" src="https://user-images.githubusercontent.com/53387856/154392630-7c1c2522-e0b6-4af4-8c82-a793c5fb65d5.png">

### 2. Frepple settings configuration
Before starting using Frepple custom app, you are required to set up certain information to enable the integration between ERPNext and Frepple.
Go to `Settings > Frepple Settings`.

- Authentication header:
> The Bearer web token key that required for REST API request. The key can be found in `Frepple Software`, under `Help > REST API Help`.

- Username and password:
> Username and password of superuser in Frepple. Default username and password are both “admin”. The information can also be found in `Frepple Software`, under `Admin > User`.


- URL:
> Web url that the user host the Frepple. The url is used for REST API request Get the wireless router IP address. You can find the Wireless LAN adapter Wi-Fi IPv4 address using `ipconfig` (Window OS) or `ifconfig` (Linux OS) command in the command prompt. E.g. http://192.168.112.1:5000.

- Frepple Integration:
> Checkbox. Tick it to turn on the automatic status syncing for sales order, work order, purchase order status and bin (stock) amount update.

- Secret key:
> Key is required for iframe embedded to render the Frepple page. Can be found under `etc/frepple/djangosettings.py` file.

## Important Note
Frepple custom app does not perform any data validation when the data are exported to Frepple software. The user must have basic knowledge of Frepple to ensure the data provided are sufficient to generate the plan in Frepple. A quick debug step is to verify the supply path matches the product structure. Remember to set up item supplier for the raw material.

## Contributors
1. [Drayang Chua Kai Yang](https://github.com/Drayang)
2. [Lee Xin Yue](https://github.com/leexy0)
3. [Chia Jun Shen](https://github.com/chiajunshen)


## License
This software is licensed under the [GNU GPLv3 LICENSE](/LICENSE) © [Selangor Human Resource Development Centre](http://www.shrdc.org.my/). 2021.  All Rights Reserved.


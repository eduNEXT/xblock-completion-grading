Completion Grading XBlock
#########################

|status-badge| |license-badge| |ci-badge|

Purpose
*******

Allows course authors to create a gradable component that will assign a
grade to students based on their level of units completion.
The instructor will be able to choose between different grading methods
and configure each of them.

This XBlock has been created as an open source contribution to the Open
edX platform and has been funded by **Unidigital** project from the Spanish
Government - 2023.

Compatibility Notes
===================

+------------------+--------------+
| Open edX Release | Version      |
+==================+==============+
| Palm             | >= 0.3.0     |
+------------------+--------------+
| Quince           | >= 0.3.0     |
+------------------+--------------+
| Redwood          | >= 0.3.0     |
+------------------+--------------+

The settings can be changed in ``completion_grading/settings/common.py`` or,
for example, in tutor configurations.

**NOTE**: the current ``common.py`` works with Open edX Palm, Quince and Redwood
version.


Enabling the XBlock in a course
*******************************

Once the XBlock has been installed in your Open edX installation, you can
enable it in a course from Studio through the **Advanced Settings**.

1. Go to Studio and open the course to which you want to add the XBlock.
2. Go to **Settings** > **Advanced Settings** from the top menu.
3. Search for **Advanced Module List** and add ``"completion_grading"``
   to the list.
4. Click **Save Changes** button.


Adding a Completion Grading Component to a course unit
*********************************************************

From Studio, you can add the Completion Grading Component to a course unit.

1. Click on the **Advanced** button in **Add New Component**.

   .. image:: https://github.com/eduNEXT/xblock-completion-grading/assets/64440265/534581c8-2120-46c1-942a-d609f8986118
      :alt: Open Advanced Components

2. Select **Completion Grading** from the list.

   .. image:: https://github.com/eduNEXT/xblock-completion-grading/assets/64440265/ed3d57d2-496f-4b78-90a2-c4d9df524241
      :alt: Select Completion Grading Component

3. Configure the component as needed.


View from the Learning Management System (CMS)
**********************************************

The **Completion Grading** component has a set of settings that can be
configured by the course author.

.. image:: https://github.com/eduNEXT/xblock-completion-grading/assets/64440265/66663034-a9f5-4119-81ca-ba5875ffebd0
    :alt: Settings for the Completion Grading component

The **Completion Grading** component has the following settings:

- **Grading Method**: Allow the course author to choose between different
  grading methods. The available options are:
  - **Minimum Completion**: grades learners based on the minimum number of
    completed units, if the learner has completed the minimum number of units,
    they will get a grade of 1, otherwise 0.
  - **Weighted Completion**: grades learners based on the weighted number of
    completed units, if the learner has completed a number of units greater or equal
    to the number of completed units required to get a grade, they will get a grade of
    1, otherwise the grade will be the number of completed units divided by the number
    of completed units required to get a grade configured in the component. The grade is
    rounded to the nearest integer.
- **Maximum Attempts**: grades learners based on the weighted number of completed units,
  if the learner has completed a number of units greater or equal to the number of
  completed units required to get a grade, they will get a grade of 1, otherwise the grade
  will be the number of completed units divided by the number of completed units required
  to get a grade configured in the component.
- **Number of Completed Units**: Allows the course author to set the number of
  number of units that need to be completed to get maximum grade.
- **Problem Weight**: Allows the course author to set the weight of the
  completion grading component in the final grade of the course.
- **Instructions Text**: Allows the course author to set the instructions that
  will be displayed to the learner.
- **Button Text**: Allows the course author to set the text that will be
  displayed on the button that the learner will use to calculate the grade.


View from the Learning Management System (LMS)
**********************************************

When a learner accesses the course, they will see the instructions and the
button to calculate the grade. If the course author has set the maximum
number of attempts, the learner will see the number of attempts left. After
the learner has calculated the grade, they will see the grade obtained.

.. image:: https://github.com/eduNEXT/xblock-completion-grading/assets/64440265/f0513817-648c-4560-bda3-5f7128b2ce0b
    :alt: View of the component in the LMS

When the learner presses the button, the grade will be calculated asynchronously based on the
selected grading method and the number of completed units. The learner must keep pressing the
button until the grade is calculated. The grade will be displayed to the learner once it is
calculated.

Experimenting with this XBlock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning
interactive components.

You can see the Completion Grading component in action in the XBlock
Workbench. Running the Workbench requires having docker running.

.. code::

    git clone git@github.com:eduNEXT/xblock-completion-grading
    virtualenv venv/
    source venv/bin/activate
    cd xblock-completion-grading
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the Completion Grading
XBlock in the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the Open edX
platform, see the `installing-the-xblock`_ documentation.

.. _XBlock: https://openedx.org/r/xblock
.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock

Getting Help
*************

If you're having trouble, the Open edX community has active completion forums
available at https://discuss.openedx.org where you can connect with others in
the community.

Also, real-time conversations are always happening on the Open edX community
Slack channel. You can request a `Slack invitation`_, then join the
`community Slack workspace`_.

For anything non-trivial, the best path is to open an `issue`_ in this
repository with as many details about the issue you are facing as you can
provide.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _issue: https://github.com/eduNEXT/xblock-completion-grading/issues
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a completion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.


Translations
============

This Xblock is initially available in English and Spanish. You can help by
translating this component to other languages. Follow the steps below:

1. Create a folder for the translations in ``locale/``, eg:
   ``locale/fr_FR/LC_MESSAGES/``, and create your ``text.po``
   file with all the translations.
2. Run ``make compile_translations``, this will generate the ``.mo`` file.
3. Create a pull request with your changes.


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email
security@edunext.co.


.. |ci-badge| image:: https://github.com/eduNEXT/xblock-completion-grading/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/eduNEXT/xblock-completion-grading/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/xblock-completion-grading.svg
    :target: https://github.com/eduNEXT/xblock-completion-grading/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen

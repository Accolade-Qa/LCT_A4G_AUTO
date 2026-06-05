from utils.logger import get_logger

logger = get_logger(__name__)


class TestUsermanagement:
    

    def test_user_management_nav_list_enability(self, user_management, report_case):
        enabled = user_management._nav_list_enability()
        report_case(expected=False, actual=enabled)
        assert enabled, "Navbar list is not enabled"

    def test_user_management_is_PageTitle_Visible(self, user_management, report_case):
        expected_title = "User Management"
        actual_title = user_management.get_title()

        report_case(expected=expected_title, actual=actual_title)
        assert (
            actual_title == expected_title
        ), f"Expected title to be '{expected_title}', got '{actual_title}'"

    def test_user_management_element_enability(self, user_management, report_case):
        ele_enabled = user_management._element_enability()

        report_case(expected=True, actual=ele_enabled)

        assert ele_enabled, "Elements not enabled"

    def test_user_management_click_add_user(self, user_management):

        user_management._click_add_user()

    def test_usermanagement_user_type_drop(self, user_management):

        error_msg = user_management.user_type_drop()

        assert (
            error_msg["result_drop_text"] == "This field is mandatory."
        ), f"Expected error message to be 'This field is mandatory.', got '{error_msg["result_drop_text"]}'"



    def test_first_name_field(self, user_management):

        result = user_management.first_name_field()

        assert result["name_blank_text"] == "This field is required and can't be empty."
        assert result["name_num_text"] == "Only alphabets and spaces are allowed."
        assert result["name_sp_char_text"] == "Only alphabets and spaces are allowed."
        assert result["name_space_text"] == "This field is required and can't be only spaces."
        assert result["name_char_space_text"] == "Remove leading or trailing spaces."
    

    def test_last_name_field(self, user_management):

        result = user_management.last_name_field()

        assert result["last_name_blank_text"] == "This field is required and can't be empty."
        assert result["last_name_num_text"] == "Only alphabets and spaces are allowed."
        assert result["last_name_sp_char_text"] == "Only alphabets and spaces are allowed."
        assert result["last_name_space_text"] == "This field is required and can't be only spaces."
        assert result["last_name_char_space_text"] == "Remove leading or trailing spaces."


    def test_email_field(self, user_management):

        result = user_management.email_field()

        assert result["email_blank_text"] == "This field is required and can't be empty."
        assert result["email_num_text"] == "Please enter a valid Email ID."
        assert result["email_sp_char_text"] == "Please enter a valid Email ID."
        assert result["email_space_text"] == "This field is required and can't be only spaces."
        assert result["email_char_space_text"] == "Please enter a valid Email ID."

    def test_mob_no_field(self, user_management):

        result = user_management.mob_no_field()

        assert result["mob_blank_text"] == "Mobile number is required."
        assert result["mob_num_text"] == "Enter a valid mobile number."
        assert result["mob_sp_char_text"] == "Enter a valid mobile number."
        assert result["mob_space_text"] == "Mobile number is required."
        assert result["mob_char_space_text"] == "Enter a valid mobile number."

    def test_country_field(self, user_management):

        result = user_management.country_field()

        assert result["con_blank_text"] == "This field is required and can't be empty."
        assert result["con_num_text"] == "Only alphabets and spaces are allowed."
        assert result["con_sp_char_text"] == "Only alphabets and spaces are allowed."
        assert result["con_space_text"] == "This field is required and can't be only spaces."
        assert result["con_char_space_text"] == "Remove leading or trailing spaces."

    def test_state_field(self, user_management):

        result = user_management.state_field()

        assert result["state_blank_text"] == "This field is required and can't be empty."
        assert result["state_num_text"] == "Only alphabets and spaces are allowed."
        assert result["state_sp_char_text"] == "Only alphabets and spaces are allowed."
        assert result["state_space_text"] == "This field is required and can't be only spaces."
        assert result["state_char_space_text"] == "Remove leading or trailing spaces."


    def test_usermanagement_status_field(self, user_management):

        error_msg = user_management.status_field()

        assert (
            error_msg["status_locator_text"] == "This field is required and can't be empty."
        ), f"Expected error message to be 'This field is required and can't be empty.', got '{error_msg["status_locator_text"]}'"

    def test_usermanagement_new_flow(self, user_management):
    
        user_management.new_flow()
    
    def test_usermanagement_update_flow(self, user_management):
    
        user_management.update_flow()
    
        
    
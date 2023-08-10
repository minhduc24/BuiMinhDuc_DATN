import Validations from "./Validations"

export default class SignupValidation {
    constructor(email, password) {
        this.email = email,
        this.password = password
    }
    
    checkValidations() {
        let errors = []

        // email validation
        if (!Validations.checkEmail(this.email)) {
            errors['email'] = 'Email không hợp lệ'
        }

        // password validation
        if (!Validations.minLength(this.password, 6)) {
            errors['password'] = 'Mật khẩu phải có 6 ký tự'
        }
        return errors
    }
} 
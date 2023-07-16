export interface RegisterType {
    first_name: string,
    last_name: string,
    user_name: string,
    email: string,
    sex: "MALE" | "FEMALE",
    birth_date: string,
    terms: boolean,
}
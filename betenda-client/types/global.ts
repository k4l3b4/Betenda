export interface UserType {
    id: number,
    first_name: string,
    last_name: string,
    user_name: string,
    email: string | undefined,
    bio: string | null,
    sex: "MALE" | "FEMALE",
    profile_avatar: string | null,
    birth_date: string,
    invited_by: number,
    phone_number: string | undefined | null,
    verified: boolean,
    has_rated: boolean,
    terms: boolean,
    is_active: boolean
    joined_date: string,
    last_login: string,
}
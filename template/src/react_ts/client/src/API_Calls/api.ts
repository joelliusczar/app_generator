import axios from "axios";
import { API_ROOT } from "../constants";

export const constructWebClient = () => {
	return axios.create({
		baseURL: API_ROOT,
		withCredentials: true,
	});
};

export const defaultWebClient = constructWebClient();

export default defaultWebClient;
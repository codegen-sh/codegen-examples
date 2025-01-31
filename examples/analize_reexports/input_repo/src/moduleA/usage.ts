import { barFunction } from './reexports';

export const useBarFunction = () => {
    console.log('Using barFunction in Module A');
    barFunction();
}; 
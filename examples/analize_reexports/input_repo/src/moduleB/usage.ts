import { Foo, utilFunctionA } from './reexports';

export const useFooAndUtil = () => {
    console.log('Using Foo and utilFunctionA in Module B');
    const fooInstance = new Foo();
    utilFunctionA();
}; 
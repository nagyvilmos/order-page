export const initialState = {};
export default function rootReducer(state = initialState, action) {
  switch (action.type) {
    default: {
      console.warn({ unhandled: action });
    }
  }
  return state;
}

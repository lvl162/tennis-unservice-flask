const dateFormat= (date) => {
    const today  = new Date(date);
    const  options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    return today.toLocaleDateString("en-US", options);
}
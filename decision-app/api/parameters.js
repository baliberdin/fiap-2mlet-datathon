class Pagination {
  page= 1;
  pageSize = 10;
  totalItems = 0;

  constructor(page, pageSize, totalItems){
    this.page = (page * 1)?page *1: 1;
    this.pageSize = (pageSize *1)? pageSize*1: 10;
    this.setTotalItems(totalItems);
  }

  setTotalItems(totalItems) {
    this.totalItems = totalItems*1? totalItems*1: 0; 
  }

  hasMorePages(){
    return (this.page * this.pageSize) < this.totalItems
  }

  getTotalPages() {
    let rest = this.totalItems % this.pageSize
    let pages = Math.floor(this.totalItems / this.pageSize)
    if(rest > 0) pages++;
    return pages;
  }

  getOffset(){
    if(this.page == 1){
      return 0;
    }

    return (this.page -1) * this.pageSize;
  }
}

module.exports = {
    Pagination
}
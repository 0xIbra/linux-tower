<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <header v-if="authStore.isAuthenticated()" class="header">
    <nav class="navbar navbar-expand-lg py-3 bg-dash-dark-2 border-bottom border-dash-dark-1 z-index-10">
      <div class="search-panel">
        <div class="search-inner d-flex align-items-center justify-content-center">
          <div class="close-btn d-flex align-items-center position-absolute top-0 end-0 me-4 mt-2 cursor-pointer"><span>Close </span>
            <svg class="svg-icon svg-icon-md svg-icon-heavy text-gray-700 mt-1">
              <use xlink:href="#close-1"> </use>
            </svg>
          </div>
          <div class="row w-100">
            <div class="col-lg-8 mx-auto">
              <form class="px-4" id="searchForm" action="#">
                <div class="input-group position-relative flex-column flex-lg-row flex-nowrap">
                  <input class="form-control shadow-0 bg-none px-0 w-100" type="search" name="search" placeholder="What are you searching for...">
                  <button class="btn btn-link text-gray-600 px-0 text-decoration-none fw-bold cursor-pointer text-center" type="submit">Search</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div class="container-fluid d-flex align-items-center justify-content-between py-1">
        <div class="navbar-header d-flex align-items-center"><a class="navbar-brand text-uppercase text-reset" href="index.html">
          <div class="brand-text brand-big"><strong class="text-primary">Linux</strong><strong>Tower</strong></div>
          <div class="brand-text brand-sm"><strong class="text-primary">L</strong><strong>T</strong></div></a>
          <button class="sidebar-toggle">
            <svg class="svg-icon svg-icon-sm svg-icon-heavy transform-none">
              <use xlink:href="#arrow-left-1"> </use>
            </svg>
          </button>
        </div>
        <ul class="list-inline mb-0">

          <!-- Messages dropdown -->
          <li class="list-inline-item dropdown px-lg-2"><a class="nav-link text-reset px-1 px-lg-0" id="navbarDropdownMenuLink1" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <svg class="svg-icon svg-icon-xs svg-icon-heavy">
              <use xlink:href="#envelope-1"> </use>
            </svg><span class="badge bg-dash-color-1">5</span></a>
            <ul class="dropdown-menu dropdown-menu-end dropdown-menu-dark" aria-labelledby="navbarDropdownMenuLink1">
              <li><a class="dropdown-item d-flex align-items-center" href="#">
                <div class="position-relative"><img class="avatar avatar-md" src="img/avatar-6.jpg" alt="Nadia Halsey">
                  <div class="availability-status bg-success"></div>
                </div>
                <div class="ms-3">   <strong class="d-block">Nadia Halsey</strong><span class="d-block text-xs">lorem ipsum dolor sit amit</span><small class="d-block">9:30am</small></div></a></li>
              <li><a class="dropdown-item d-flex align-items-center" href="#">
                <div class="position-relative"><img class="avatar avatar-md" src="img/avatar-6.jpg" alt="Peter Ramsy">
                  <div class="availability-status bg-warning"></div>
                </div>
                <div class="ms-3">   <strong class="d-block">Nadia Halsey</strong><span class="d-block text-xs">lorem ipsum dolor sit amit</span><small class="d-block">9:30am</small></div></a></li>
              <li><a class="dropdown-item d-flex align-items-center" href="#">
                <div class="position-relative"><img class="avatar avatar-md" src="img/avatar-6.jpg" alt="Sam Kaheil">
                  <div class="availability-status bg-danger"></div>
                </div>
                <div class="ms-3">   <strong class="d-block">Nadia Halsey</strong><span class="d-block text-xs">lorem ipsum dolor sit amit</span><small class="d-block">9:30am</small></div></a></li>
              <li><a class="dropdown-item d-flex align-items-center" href="#">
                <div class="position-relative"><img class="avatar avatar-md" src="img/avatar-6.jpg" alt="Sara Wood">
                  <div class="availability-status bg-secondary"></div>
                </div>
                <div class="ms-3">   <strong class="d-block">Nadia Halsey</strong><span class="d-block text-xs">lorem ipsum dolor sit amit</span><small class="d-block">9:30am</small></div></a></li>
              <li><a class="dropdown-item text-center message" href="#"> <strong>See All Messages <i class="fas fa-angle-right ms-1"></i></strong></a></li>
            </ul>
          </li>
          <!-- Tasks dropdown                   -->
          <li class="list-inline-item dropdown px-lg-2"><a class="nav-link text-reset px-1 px-lg-0" id="navbarDropdownMenuLink2" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <svg class="svg-icon svg-icon-xs svg-icon-heavy">
              <use xlink:href="#paper-stack-1"> </use>
            </svg><span class="badge bg-dash-color-3">9</span></a>
            <ul class="dropdown-menu dropdown-menu-end dropdown-menu-dark" aria-labelledby="navbarDropdownMenuLink2">
              <li><a class="dropdown-item" href="#">
                <div class="d-flex justify-content-between mb-1"><strong>Task 1</strong><span>40% complete</span></div>
                <div class="progress" style="height: 2px">
                  <div class="progress-bar bg-dash-color-1" role="progressbar" style="width: 40%" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100"></div>
                </div></a></li>
              <li><a class="dropdown-item" href="#">
                <div class="d-flex justify-content-between mb-1"><strong>Task 2</strong><span>20% complete</span></div>
                <div class="progress" style="height: 2px">
                  <div class="progress-bar bg-dash-color-2" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div></a></li>
              <li><a class="dropdown-item" href="#">
                <div class="d-flex justify-content-between mb-1"><strong>Task 3</strong><span>70% complete</span></div>
                <div class="progress" style="height: 2px">
                  <div class="progress-bar bg-dash-color-3" role="progressbar" style="width: 70%" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100"></div>
                </div></a></li>
              <li><a class="dropdown-item" href="#">
                <div class="d-flex justify-content-between mb-1"><strong>Task 4</strong><span>40% complete</span></div>
                <div class="progress" style="height: 2px">
                  <div class="progress-bar bg-dash-color-4" role="progressbar" style="width: 40%" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100"></div>
                </div></a></li>
              <li><a class="dropdown-item" href="#">
                <div class="d-flex justify-content-between mb-1"><strong>Task 5</strong><span>30% complete</span></div>
                <div class="progress" style="height: 2px">
                  <div class="progress-bar bg-dash-color-1" role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                </div></a></li>
              <li>           <a class="dropdown-item text-center" href="#"> <strong>See All Tasks <i class="fas fa-angle-right ms-1"></i></strong></a></li>
            </ul>
          </li>

          <li class="list-inline-item logout px-lg-2">
            <a class="nav-link text-sm text-reset px-1 px-lg-0 cursor-pointer" id="logout" @click="authStore.reset()">
              <span class="d-none d-sm-inline-block">Logout</span>
            </a>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>